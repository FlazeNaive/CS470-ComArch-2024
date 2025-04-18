# CS-470 Homework 2
This folder contains all the necessary material to complete the homework 2 of the CS-470 course.

- The homework handout.
- A set of test cases to help you ensure your code is correct, under given_tests.
- A Dockerfile containing the grading environment.
- A runall.sh script to run your code using the provided test, and a testall.sh script to test your code against the
  provided tests.
- An html visualizer you can use to visualize the schedules generated by your code.

## Running Your Code
We provide basic tests cases for you to test your code, which are under the test folder. You can check desc.txt under
each folder to see their description. 

Assuming you already have a valid build.sh and run.sh script, you can run generate the schedules corresponding to all
test cases using.

```
./runall.sh
```

And you can test your code against the reference using.

```
./testall.sh
```

## Docker Image
We provide you with a docker image containing the environment we will use for grading. Please ensure that your code
compiles and runs within the docker environment before submitting. 

To install docker on your system please follow the instructions on the docker website. We will assume over the next
instructions that you have a valid docker installation. You can check that your docker installation is working with: 

```
sudo docker run hello-world
```

The grading environment is defined in a configuration file called Dockerfile. With it, we can build the docker image
docker containing the actual grading environment and register it to docker. We can do so with two commands.

From the root of the homework (where the Dockerfile image is), to build the docker image simply run.

```
sudo docker build . -t cs470
```

After which, you should see the image under the name cs470 when running.

```
sudo docker image ls
```

You docker setup is now complete. From this point, you only need to run the following command to run the grading
environment (from the root of the homework project). 

```
sudo docker run -it -v $(pwd):/home/root/cs470 cs470
```

Where we mount the root of the project in /home/root/cs470 in the docker image. You can then check that your code runs
in the environment as follows. 

```
cd /home/root/cs470
./runall.sh
./testall.sh
```

If you have any questions when installing / running docker, please talk to a TA, we would be happy
to help.


For Test
```
basic one:
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/12/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/12/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/12/pip_mine.json


./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/02/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/02/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/02/pip_mine.json

with loop:
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/04/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/04/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/04/pip_mine.json

./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/09/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/09/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/09/pip_mine.json

has dependencies:
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/10/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/10/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/10/pip_mine.json

has interloop dependency:
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/11/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/11/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/11/pip_mine.json

single invar:
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/13/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/13/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/13/pip_mine.json


./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/14/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/14/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/14/pip_mine.json

# 自定义
./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/18/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/18/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/18/pip_mine.json

./run.sh /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/19/input.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/19/simple_mine.json /home/flaze/semester4/CS470-Homeworks-2024/HW2/given_tests/19/pip_mine.json
```
