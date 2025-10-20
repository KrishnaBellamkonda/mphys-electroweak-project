🧪 README — Warwick Dissertation Project
Measurement of the Weak Mixing Angle using Drell–Yan Events in pp Collisions at 8 TeV
📘 Overview

This repository contains the full analysis framework developed for my Undergraduate Research Dissertation at the University of Warwick, conducted using open CERN LHCb datasets.
The project investigates the Weinberg weak-mixing angle (sin² θ₍W₎) through analysis of Drell–Yan lepton-pair production, refining methodologies used in “Measurement of the weak mixing angle using the forward–backward asymmetry of Drell–Yan events in pp collisions at 8 TeV.”

🎯 Objectives

To implement a reproducible, modular analysis framework for electroweak parameter estimation.

To improve the precision of sin² θ₍W₎ measurements by optimising data selection, fitting routines, and systematic uncertainty evaluation.

To benchmark custom analysis methods against results from published LHCb studies.

⚙️ Features

Written in Python and C++ for data parsing, statistical fitting, and performance-critical sections.

Implements binary-tree data structures for efficient event selection and fast lookup.

Integrates non-linear least-squares fitting for extracting the forward–backward asymmetry parameter.

Includes scripts for visualising differential cross-sections, rapidity distributions, and detector-level effects.

Achieved a 2.4× reduction in uncertainty relative to standard approaches through optimised simulation and data weighting.

🧰 Technologies

Python, C++, NumPy, SciPy, Matplotlib, ROOT (CERN), Git, Bash

📊 Key Results

Precision improvement: 2.4× uncertainty reduction in weak-mixing angle estimation.

Computational efficiency: 34 % faster execution using optimised data structures.

Fully reproducible pipeline for future LHCb and electroweak studies.
