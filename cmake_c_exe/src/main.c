#include <stdlib.h>
#include <stddef.h>
#include <argp.h>
#include <time.h>

#include "version.h"

typedef struct Parameters_ {
	int version;
} Parameters;

static error_t parse_opt(int key, char *arg, struct argp_state *state)
{
	/* Get the input argument from argp_parse, which we
	know is a pointer to our arguments structure. */
	Parameters *arguments = state->input;
	switch (key) {
	case 'v':
		arguments->version = 1;
		break;
	case ARGP_KEY_ARG:
		// if (state->arg_num >= 1)
		// 	/* Too many arguments. */
		// 	argp_usage(state);
		break;
	case ARGP_KEY_END:
		// if (state->arg_num < 1)
		// 	/* Not enough arguments. */
		// 	argp_usage(state);
		break;
	default:
		return ARGP_ERR_UNKNOWN;
	}
	return 0;
}

int main(int argc, char **argv)
{
	Parameters params;

	/* Default arguments */
	params.version = 0;
	/* ----------------- */

	struct argp_option options[] = {
		{ "version", 'v', NULL, 0, "Print version string" },
		{ 0 }
	};
	char *doc = "<description here>";
	struct argp argp = {
		options,
		parse_opt,
		NULL,
		doc
	};
	argp_parse(&argp, argc, argv, 0, 0, &params);

	if(params.version){
		printf("Version: %s", VERSION);
	}

	return EXIT_SUCCESS;
}
