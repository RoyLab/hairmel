#ifdef _DEBUG
#undef _DEBUG
#include <Python.h>
#define _DEBUG
#else
#include <Python.h>
#endif
#include <cyHairFile.h>
#include <arrayobject.h>
#include <fstream>

#include "macros.h"


static PyObject* loadHairZhou(PyObject* self, PyObject* args)
{
	const char* fileName;
	if (!PyArg_ParseTuple(args, "s", &fileName))  return NULL;

	std::ifstream hairfile(fileName, std::ios::binary);

	if (!hairfile.is_open())
	{
		printf("Error: Cannot open hair file %s!\n", fileName);
		Py_RETURN_NONE;
	}

	int hairCount, pointCount;
	Read4Bytes(hairfile, pointCount);

	npy_intp dims[1] = { pointCount * 3 };
	PyArrayObject* pos = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_FLOAT);
	ReadNBytes(hairfile, PyArray_DATA(pos), sizeof(float) * dims[0]);

	Read4Bytes(hairfile, hairCount);

	dims[0] = hairCount;
	PyArrayObject* idx = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_INT);
	ReadNBytes(hairfile, PyArray_DATA(idx), sizeof(int) * dims[0]);

	hairfile.close();
	return Py_BuildValue("(OOii)", pos, idx, hairCount, pointCount);
}

static PyObject* loadHair(PyObject* self, PyObject* args)
{
	const char* fileName;
	if (!PyArg_ParseTuple(args, "s", &fileName))  return NULL;

	cyHairFile hairfile;
	int result = hairfile.LoadFromFile(fileName);

	// Check for errors
	switch (result) {
	case CY_HAIR_FILE_ERROR_CANT_OPEN_FILE:
		printf("Error: Cannot open hair file %s!\n", fileName);
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_CANT_READ_HEADER:
		printf("Error: Cannot read hair file header!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_WRONG_SIGNATURE:
		printf("Error: File has wrong signature!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_READING_SEGMENTS:
		printf("Error: Cannot read hair segments!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_READING_POINTS:
		printf("Error: Cannot read hair points!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_READING_COLORS:
		printf("Error: Cannot read hair colors!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_READING_THICKNESS:
		printf("Error: Cannot read hair thickness!\n");
		Py_RETURN_NONE;
	case CY_HAIR_FILE_ERROR_READING_TRANSPARENCY:
		printf("Error: Cannot read hair transparency!\n");
		Py_RETURN_NONE;
	default:
		printf("Hair file \"%s\" loaded.\n", fileName);
	}

	int hairCount = hairfile.GetHeader().hair_count;
	int pointCount = hairfile.GetHeader().point_count;

	printf("Number of hair strands = %d\n", hairCount);
	printf("Number of hair points = %d\n", pointCount);

	npy_intp dims[1] = { pointCount *3};
	PyArrayObject* pos = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_FLOAT);
	memcpy(PyArray_DATA(pos), hairfile.GetPointsArray(), sizeof(float) * dims[0]);

	dims[0] = hairCount;
	PyArrayObject* idx = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_USHORT);
	memcpy(PyArray_DATA(idx), hairfile.GetSegmentsArray(), sizeof(unsigned short) * dims[0]);

	return Py_BuildValue("(OOii)", pos, idx, hairCount, pointCount);
}

static PyObject* random(PyObject* self, PyObject* args)
{
	/* initialize random seed: */
	srand(time(NULL));
	int random = rand() % 10;
	PyObject * python_val = Py_BuildValue("i", random);
	return python_val;
}

PyMODINIT_FUNC initpyhair(void)
{
	static PyMethodDef methods[] = {
		{ "random", random, METH_NOARGS,
		"Generate random number betweeen 0-9" },
		{ "loadHair", loadHair, METH_VARARGS,
		"Load hair file by name" },
		{ "loadHairZhou", loadHairZhou, METH_VARARGS,
		"Load hair file by name, Zhou's style" },
		{ NULL, NULL, 0, NULL }
	};

	PyObject *m = Py_InitModule("pyhair", methods);
	import_array();
}