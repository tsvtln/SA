#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>

/*

INSTALLATION:

gcc -Wall -W -pedantic -O2 -o twinpipe twinpipe.c
cp -p twinpipe /usr/local/bin/
ln -f /usr/local/bin/twinpipe /usr/local/bin/usleep

*/

static int pipe1[2], pipe2[2];
static void sulje(void)
{
	close(pipe2[0]); close(pipe2[1]);
	close(pipe1[0]); close(pipe1[1]);
}

static int pid1, pid2;

static void die(int n)
{
	kill(pid1, n);
	kill(pid2, n);
}

int main(int argc, const char *const *argv)
{
	int pid1,pid2, sid;
	const char *fail="";
	
	if(argc != 3)
	{
		if(argc == 2)
		{
			int i = atoi(argv[1]);
			if(i) { usleep(i); return 0; /* usleep */ }
		}
		fprintf(stderr,
			"Usage: usleep microseconds\n"
			"Usage: twinpipe 'command1' 'command2'\n"
			"The commands will be able to read each others output.\n");
		return -1;
	}
	
	signal(1, die);
	signal(2, die);
	signal(11, die);
	signal(13, die);
	signal(15, die);
	
	if((sid = setsid()) < 0)sid = getpgrp();
	
	if((sid < 0 && (fail = "sid"))
     || (pipe(pipe1) < 0 && (fail = "pipe1"))
     || (pipe(pipe2) < 0 && (fail = "pipe2")))
    {
collapsed:
		fprintf(stderr, "Ouch, the world just collapsed (%s).\n", fail);
		perror(*argv);
		return -1;
	}
	
	fcntl(pipe1[0], F_SETFL, fcntl(pipe1[0], F_GETFL) & ~O_NONBLOCK);
	fcntl(pipe1[1], F_SETFL, fcntl(pipe1[1], F_GETFL) & ~O_NONBLOCK);
	fcntl(pipe2[0], F_SETFL, fcntl(pipe2[0], F_GETFL) & ~O_NONBLOCK);
	fcntl(pipe2[1], F_SETFL, fcntl(pipe2[1], F_GETFL) & ~O_NONBLOCK);
	
	if((pid1 = fork()) < 0)goto collapsed;	
	if(pid1)
		setpgid(pid1, sid);
	else
	{
		dup2(pipe1[0], 0);
		dup2(pipe2[1], 1);
		sulje();
		execl("/bin/sh", "sh", "-c", argv[1], NULL);
		_exit(0);
	}

	if((pid2 = fork()) < 0)goto collapsed;	
	if(pid2)
		setpgid(pid2, sid);
	else
	{
		dup2(pipe2[0], 0);
		dup2(pipe1[1], 1);
		sulje();
		execl("/bin/sh", "sh", "-c", argv[2], NULL);
		_exit(0);
	}
	
	sulje();
	
	while(wait(NULL) >= 0);
	
	return 0;
}
