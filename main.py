#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import gmres
import interative_integral
import read_problem


def main():

    file = open("problem.txt", "r")
    problem = file.read()

    print("O problema é : ",problem)

    print("Resultado") 

main()