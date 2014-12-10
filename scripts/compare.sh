#!/usr/bin/env sh

exec diff -u $@ | cdiff
