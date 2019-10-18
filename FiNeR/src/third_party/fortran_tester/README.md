# Fortran tester {#mainpage}

`tester` is a Fortran module to test Fortran programs. It provides routines to
check equality or closeness between variables and counting the errors.

A minimal example:

	program test
	  use tester
	  implicit none

	  type(tester_t) :: my_tester

	  call my_tester% init()

	  call my_tester% assert_equal(1, 2, fail=.true.)

	  call my_tester% print()

	end program test

If none of the tests fail, the `print` method displays the message
`fortran_tester: all tests succeeded`.
Else, the program will exit with a nonzero error code, making it suitable for
use as an automated test.

**Author:** Pierre de Buyl  
**License:** BSD

Contributors: Peter Colberg, Stefano Szaghi, Pietro Bonfa, Elias Lettl

## Installation

`fortran_tester` consists of a single Fortran file. You can just drop `src/tester.f90` in
your Fortran project or build using [CMake](https://cmake.org/) or
[FoBiS](https://github.com/szaghi/FoBiS).

## Coverage information

If you read the autogenerated documentation, the [coverage
data](ft_coverage/index.html) should be available.