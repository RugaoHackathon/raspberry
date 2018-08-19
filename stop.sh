#!/bin/bash
kill -9 `ps -ef | grep python | awk -F ' ' '{print $2}'`