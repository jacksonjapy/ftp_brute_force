#define _GNU_SOURCE
#include <Python.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    PyObject_HEAD
    FILE    *user_file_pointer;         // User dictionary file pointer
    FILE    *password_file_pointer;     // Password dictionary file pointer
    char    *user_buffer;               // getline user buffer
    size_t   user_buffer_capacity;
    char    *password_buffer;           // getline password buffer
    size_t   password_buffer_capacity;
    PyObject *current_user;             // Current user string
} StreamIterator;

// Destructor: close files, free buffers, DECREF current_user
static void
StreamIterator_dealloc(StreamIterator *self)
{
    if (self->user_file_pointer) fclose(self->user_file_pointer);
    if (self->password_file_pointer) fclose(self->password_file_pointer);
    PyMem_Free(self->user_buffer);
    PyMem_Free(self->password_buffer);
    Py_XDECREF(self->current_user);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

// __next__: return (user, pwd) tuple
static PyObject *
StreamIterator_iternext(StreamIterator *self)
{
    // If current_user is NULL, read the first line of user
    if (!self->current_user) {
        ssize_t user_line_length;
        do {
            user_line_length = getline(&self->user_buffer, &self->user_buffer_capacity, self->user_file_pointer);
            if (user_line_length <= 0) {
                PyErr_SetNone(PyExc_StopIteration);
                return NULL;
            }
            // Remove newline
            while (user_line_length > 0 && (self->user_buffer[user_line_length-1] == '\n' || self->user_buffer[user_line_length-1] == '\r'))
                self->user_buffer[--user_line_length] = '\0';
        } while (user_line_length == 0 || self->user_buffer[0] == '#' || (user_line_length >= 2 && self->user_buffer[0] == '/' && self->user_buffer[1] == '/'));

        self->current_user = PyUnicode_FromStringAndSize(self->user_buffer, user_line_length);
        if (!self->current_user) return NULL;
        // Reset password file to the beginning
        fseek(self->password_file_pointer, 0, SEEK_SET);
    }

    // Read one line of password
    ssize_t password_line_length;
    do {
        password_line_length = getline(&self->password_buffer, &self->password_buffer_capacity, self->password_file_pointer);
        if (password_line_length <= 0) {
            // Password file EOF: prepare next user
            Py_DECREF(self->current_user);
            self->current_user = NULL;
            return StreamIterator_iternext(self);
        }
        // Remove newline
        while (password_line_length > 0 && (self->password_buffer[password_line_length-1] == '\n' || self->password_buffer[password_line_length-1] == '\r'))
            self->password_buffer[--password_line_length] = '\0';
    } while (password_line_length == 0 || self->password_buffer[0] == '#' || (password_line_length >= 2 && self->password_buffer[0] == '/' && self->password_buffer[1] == '/'));

    PyObject *py_pwd = PyUnicode_FromStringAndSize(self->password_buffer, password_line_length);
    if (!py_pwd) return NULL;

    // Pack (user, pwd)
    PyObject *tup = PyTuple_Pack(2, self->current_user, py_pwd);
    Py_DECREF(py_pwd);
    return tup;
}

static PyTypeObject StreamIteratorType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name      = "load_dict.StreamIterator",
    .tp_basicsize = sizeof(StreamIterator),
    .tp_dealloc   = (destructor)StreamIterator_dealloc,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_iter      = PyObject_SelfIter,
    .tp_iternext  = (iternextfunc)StreamIterator_iternext,
};

// load_stream(user_path, pass_path) -> StreamIterator
static PyObject *
load_dict(PyObject *self, PyObject *args)
{
    const char *user_path, *password_path;
    if (!PyArg_ParseTuple(args, "ss", &user_path, &password_path))
        return NULL;

    FILE *uf = fopen(user_path, "r");
    if (!uf) {
        PyErr_SetFromErrnoWithFilename(PyExc_IOError, user_path);
        return NULL;
    }
    FILE *pf = fopen(password_path, "r");
    if (!pf) {
        fclose(uf);
        PyErr_SetFromErrnoWithFilename(PyExc_IOError, password_path);
        return NULL;
    }

    StreamIterator *it = PyObject_New(StreamIterator, &StreamIteratorType);
    it->user_file_pointer = uf;
    it->password_file_pointer = pf;
    it->user_buffer = NULL;
    it->user_buffer_capacity = 0;
    it->password_buffer = NULL;
    it->password_buffer_capacity = 0;
    it->current_user = NULL;
    return (PyObject*)it;
}

static PyMethodDef LoadDictMethods[] = {
    {"load_dict", load_dict, METH_VARARGS,
     "Stream loads user/password dictionaries, suitable for scenarios larger than 500MB. Returns an iterator of (user, password)."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef load_dict_module = {
    PyModuleDef_HEAD_INIT,
    "load_dict",
    NULL,
    -1,
    LoadDictMethods
};

PyMODINIT_FUNC
PyInit_load_dict(void)
{
    if (PyType_Ready(&StreamIteratorType) < 0)
        return NULL;
    return PyModule_Create(&load_dict_module);
}