#include <iostream>
#include <cyHairFile.h>

using namespace std;
using namespace cy;

void LoadHairModel(const char *filename, cyHairFile &hairfile, float *&dirs)
{
	// Load the hair model
	int result = hairfile.LoadFromFile(filename);

	// Check for errors
	switch (result) {
	case CY_HAIR_FILE_ERROR_CANT_OPEN_FILE:
		printf("Error: Cannot open hair file!\n");
		return;
	case CY_HAIR_FILE_ERROR_CANT_READ_HEADER:
		printf("Error: Cannot read hair file header!\n");
		return;
	case CY_HAIR_FILE_ERROR_WRONG_SIGNATURE:
		printf("Error: File has wrong signature!\n");
		return;
	case CY_HAIR_FILE_ERROR_READING_SEGMENTS:
		printf("Error: Cannot read hair segments!\n");
		return;
	case CY_HAIR_FILE_ERROR_READING_POINTS:
		printf("Error: Cannot read hair points!\n");
		return;
	case CY_HAIR_FILE_ERROR_READING_COLORS:
		printf("Error: Cannot read hair colors!\n");
		return;
	case CY_HAIR_FILE_ERROR_READING_THICKNESS:
		printf("Error: Cannot read hair thickness!\n");
		return;
	case CY_HAIR_FILE_ERROR_READING_TRANSPARENCY:
		printf("Error: Cannot read hair transparency!\n");
		return;
	default:
		printf("Hair file \"%s\" loaded.\n", filename);
	}

	int hairCount = hairfile.GetHeader().hair_count;
	int pointCount = hairfile.GetHeader().point_count;
	printf("Number of hair strands = %d\n", hairCount);
	printf("Number of hair points = %d\n", pointCount);

	// Compute directions
	dirs = new float[3 * pointCount];
	if (hairfile.FillDirectionArray(dirs) == 0) {
		printf("Error: Cannot compute hair directions!\n");
	}
}

int main()
{
	cyHairFile hair;
	float *dirs;
	LoadHairModel("D:\\Data\\modelimport\\wWavyThin.hair", hair, dirs);
	delete[]dirs;
	return 0;
}