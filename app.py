from flask import Flask, render_template, jsonify
import os
import glob
import re
from datetime import datetime

print("CURRENT PATH =", os.getcwd())
app = Flask(__name__)

# Main reflow profile folder
ROOT_FOLDER = r"N:\Electronics\SMT\94.SRA PROFILE"

# Spec is embedded from std.txt: Air/Mass LCL, STD, UCL and Conveyor LCL/UCL
SPEC_CACHE = {'air': {'Line1': {1: {'lcl': 104.0, 'std': 109.0, 'ucl': 114.0},
                   2: {'lcl': 126.7, 'std': 129.2, 'ucl': 131.7},
                   3: {'lcl': 148.3, 'std': 150.8, 'ucl': 153.3},
                   4: {'lcl': 160.1, 'std': 162.6, 'ucl': 165.1},
                   5: {'lcl': 172.3, 'std': 174.8, 'ucl': 177.3},
                   6: {'lcl': 182.5, 'std': 185.0, 'ucl': 187.5},
                   7: {'lcl': 194.5, 'std': 197.0, 'ucl': 199.5},
                   8: {'lcl': 203.6, 'std': 206.1, 'ucl': 208.6},
                   9: {'lcl': 213.5, 'std': 216.0, 'ucl': 218.5},
                   10: {'lcl': 230.0, 'std': 232.5, 'ucl': 235.0},
                   11: {'lcl': 244.0, 'std': 246.5, 'ucl': 249.0},
                   12: {'lcl': 256.8, 'std': 259.3, 'ucl': 261.8}},
         'Line10': {1: {'lcl': 102.7, 'std': 107.7, 'ucl': 112.7},
                    2: {'lcl': 122.8, 'std': 125.3, 'ucl': 127.8},
                    3: {'lcl': 132.1, 'std': 134.6, 'ucl': 137.1},
                    4: {'lcl': 148.4, 'std': 150.9, 'ucl': 153.4},
                    5: {'lcl': 159.4, 'std': 161.9, 'ucl': 164.4},
                    6: {'lcl': 170.5, 'std': 173.0, 'ucl': 175.5},
                    7: {'lcl': 180.7, 'std': 183.2, 'ucl': 185.7},
                    8: {'lcl': 192.0, 'std': 194.5, 'ucl': 197.0},
                    9: {'lcl': 201.9, 'std': 204.4, 'ucl': 206.9},
                    10: {'lcl': 215.2, 'std': 217.7, 'ucl': 220.2},
                    11: {'lcl': 219.2, 'std': 229.0, 'ucl': 232.0},
                    12: {'lcl': 215.2, 'std': 215.2, 'ucl': 215.2}},
         'Line2': {1: {'lcl': 104.2, 'std': 109.2, 'ucl': 114.2},
                   2: {'lcl': 129.5, 'std': 132.0, 'ucl': 134.5},
                   3: {'lcl': 148.4, 'std': 150.9, 'ucl': 153.4},
                   4: {'lcl': 160.6, 'std': 163.1, 'ucl': 165.6},
                   5: {'lcl': 171.6, 'std': 174.1, 'ucl': 176.6},
                   6: {'lcl': 181.5, 'std': 184.0, 'ucl': 186.5},
                   7: {'lcl': 193.0, 'std': 195.5, 'ucl': 198.0},
                   8: {'lcl': 200.7, 'std': 203.2, 'ucl': 205.7},
                   9: {'lcl': 211.6, 'std': 214.1, 'ucl': 216.6},
                   10: {'lcl': 226.9, 'std': 229.4, 'ucl': 231.9},
                   11: {'lcl': 239.6, 'std': 242.1, 'ucl': 244.6},
                   12: {'lcl': 249.3, 'std': 251.8, 'ucl': 254.3}},
         'Line3': {1: {'lcl': 105.8, 'std': 110.8, 'ucl': 115.8},
                   2: {'lcl': 128.2, 'std': 130.7, 'ucl': 133.2},
                   3: {'lcl': 147.7, 'std': 150.2, 'ucl': 152.7},
                   4: {'lcl': 159.6, 'std': 162.1, 'ucl': 164.6},
                   5: {'lcl': 171.8, 'std': 174.3, 'ucl': 176.8},
                   6: {'lcl': 182.8, 'std': 185.3, 'ucl': 187.8},
                   7: {'lcl': 194.6, 'std': 197.1, 'ucl': 199.6},
                   8: {'lcl': 203.9, 'std': 206.4, 'ucl': 208.9},
                   9: {'lcl': 214.3, 'std': 216.8, 'ucl': 219.3},
                   10: {'lcl': 230.0, 'std': 232.5, 'ucl': 235.0},
                   11: {'lcl': 244.6, 'std': 247.1, 'ucl': 249.6},
                   12: {'lcl': 258.1, 'std': 260.6, 'ucl': 263.1}},
         'Line4': {1: {'lcl': 100.1, 'std': 105.1, 'ucl': 110.1},
                   2: {'lcl': 126.2, 'std': 128.7, 'ucl': 131.2},
                   3: {'lcl': 148.4, 'std': 150.9, 'ucl': 153.4},
                   4: {'lcl': 161.1, 'std': 163.6, 'ucl': 166.1},
                   5: {'lcl': 173.0, 'std': 175.5, 'ucl': 178.0},
                   6: {'lcl': 183.6, 'std': 186.1, 'ucl': 188.6},
                   7: {'lcl': 194.8, 'std': 197.3, 'ucl': 199.8},
                   8: {'lcl': 202.7, 'std': 205.2, 'ucl': 207.7},
                   9: {'lcl': 214.7, 'std': 217.2, 'ucl': 219.7},
                   10: {'lcl': 232.0, 'std': 234.5, 'ucl': 237.0},
                   11: {'lcl': 245.2, 'std': 247.7, 'ucl': 250.2},
                   12: {'lcl': 256.4, 'std': 258.9, 'ucl': 261.4}},
         'Line5': {1: {'lcl': 98.9, 'std': 103.9, 'ucl': 108.9},
                   2: {'lcl': 124.5, 'std': 127.0, 'ucl': 129.5},
                   3: {'lcl': 146.2, 'std': 148.7, 'ucl': 151.2},
                   4: {'lcl': 158.2, 'std': 160.7, 'ucl': 163.2},
                   5: {'lcl': 171.2, 'std': 173.7, 'ucl': 176.2},
                   6: {'lcl': 182.7, 'std': 185.2, 'ucl': 187.7},
                   7: {'lcl': 192.8, 'std': 195.3, 'ucl': 197.8},
                   8: {'lcl': 202.5, 'std': 205.0, 'ucl': 207.5},
                   9: {'lcl': 213.7, 'std': 216.2, 'ucl': 218.7},
                   10: {'lcl': 229.6, 'std': 232.1, 'ucl': 234.6},
                   11: {'lcl': 242.7, 'std': 245.2, 'ucl': 247.7},
                   12: {'lcl': 254.9, 'std': 257.4, 'ucl': 259.9}},
         'Line6': {1: {'lcl': 104.8, 'std': 109.8, 'ucl': 114.8},
                   2: {'lcl': 128.4, 'std': 130.9, 'ucl': 133.4},
                   3: {'lcl': 150.0, 'std': 152.5, 'ucl': 155.0},
                   4: {'lcl': 162.1, 'std': 164.6, 'ucl': 167.1},
                   5: {'lcl': 174.3, 'std': 176.8, 'ucl': 179.3},
                   6: {'lcl': 184.4, 'std': 186.9, 'ucl': 189.4},
                   7: {'lcl': 195.5, 'std': 198.0, 'ucl': 200.5},
                   8: {'lcl': 204.8, 'std': 207.3, 'ucl': 209.8},
                   9: {'lcl': 213.9, 'std': 216.4, 'ucl': 218.9},
                   10: {'lcl': 229.2, 'std': 231.7, 'ucl': 234.2},
                   11: {'lcl': 243.6, 'std': 246.1, 'ucl': 248.6},
                   12: {'lcl': 250.8, 'std': 253.3, 'ucl': 255.8}},
         'Line7': {1: {'lcl': 101.7, 'std': 106.7, 'ucl': 111.7},
                   2: {'lcl': 129.5, 'std': 132.0, 'ucl': 134.5},
                   3: {'lcl': 150.1, 'std': 152.6, 'ucl': 155.1},
                   4: {'lcl': 161.9, 'std': 164.4, 'ucl': 166.9},
                   5: {'lcl': 173.2, 'std': 175.7, 'ucl': 178.2},
                   6: {'lcl': 184.7, 'std': 187.2, 'ucl': 189.7},
                   7: {'lcl': 195.6, 'std': 198.1, 'ucl': 200.6},
                   8: {'lcl': 203.1, 'std': 205.6, 'ucl': 208.1},
                   9: {'lcl': 214.2, 'std': 216.7, 'ucl': 219.2},
                   10: {'lcl': 230.0, 'std': 232.5, 'ucl': 235.0},
                   11: {'lcl': 244.0, 'std': 246.5, 'ucl': 249.0},
                   12: {'lcl': 255.9, 'std': 258.4, 'ucl': 260.9}},
         'Line8': {1: {'lcl': 102.7, 'std': 107.7, 'ucl': 112.7},
                   2: {'lcl': 128.0, 'std': 130.5, 'ucl': 133.0},
                   3: {'lcl': 148.6, 'std': 151.1, 'ucl': 153.6},
                   4: {'lcl': 161.0, 'std': 163.5, 'ucl': 166.0},
                   5: {'lcl': 172.8, 'std': 175.3, 'ucl': 177.8},
                   6: {'lcl': 184.6, 'std': 187.1, 'ucl': 189.6},
                   7: {'lcl': 195.1, 'std': 197.6, 'ucl': 200.1},
                   8: {'lcl': 203.5, 'std': 206.0, 'ucl': 208.5},
                   9: {'lcl': 215.5, 'std': 218.0, 'ucl': 220.5},
                   10: {'lcl': 230.3, 'std': 232.8, 'ucl': 235.3},
                   11: {'lcl': 243.2, 'std': 245.7, 'ucl': 248.2},
                   12: {'lcl': 256.9, 'std': 259.4, 'ucl': 261.9}},
         'Line9': {1: {'lcl': 88.1, 'std': 93.1, 'ucl': 98.1},
                   2: {'lcl': 123.2, 'std': 125.7, 'ucl': 128.2},
                   3: {'lcl': 141.0, 'std': 143.5, 'ucl': 146.0},
                   4: {'lcl': 154.3, 'std': 156.8, 'ucl': 159.3},
                   5: {'lcl': 166.1, 'std': 168.6, 'ucl': 171.1},
                   6: {'lcl': 183.3, 'std': 185.8, 'ucl': 188.3},
                   7: {'lcl': 195.6, 'std': 198.1, 'ucl': 200.6},
                   8: {'lcl': 219.0, 'std': 221.5, 'ucl': 224.0},
                   9: {'lcl': 237.3, 'std': 239.8, 'ucl': 242.3}}},
 'mass': {'Line1': {1: {'lcl': 44.5, 'std': 49.5, 'ucl': 54.5},
                    2: {'lcl': 66.0, 'std': 71.0, 'ucl': 76.0},
                    3: {'lcl': 86.4, 'std': 91.4, 'ucl': 96.4},
                    4: {'lcl': 105.0, 'std': 110.0, 'ucl': 115.0},
                    5: {'lcl': 121.5, 'std': 126.5, 'ucl': 131.5},
                    6: {'lcl': 136.3, 'std': 141.3, 'ucl': 146.3},
                    7: {'lcl': 150.0, 'std': 155.0, 'ucl': 160.0},
                    8: {'lcl': 162.6, 'std': 167.6, 'ucl': 172.6},
                    9: {'lcl': 174.5, 'std': 179.5, 'ucl': 184.5},
                    10: {'lcl': 187.7, 'std': 192.7, 'ucl': 197.7},
                    11: {'lcl': 201.2, 'std': 206.2, 'ucl': 211.2},
                    12: {'lcl': 212.6, 'std': 217.6, 'ucl': 222.6}},
          'Line10': {1: {'lcl': 41.0, 'std': 46.0, 'ucl': 51.0},
                     2: {'lcl': 57.6, 'std': 62.6, 'ucl': 67.6},
                     3: {'lcl': 73.2, 'std': 78.2, 'ucl': 83.2},
                     4: {'lcl': 87.4, 'std': 92.4, 'ucl': 97.4},
                     5: {'lcl': 100.0, 'std': 105.0, 'ucl': 110.0},
                     6: {'lcl': 113.0, 'std': 118.0, 'ucl': 123.0},
                     7: {'lcl': 125.6, 'std': 130.6, 'ucl': 135.6},
                     8: {'lcl': 137.6, 'std': 142.6, 'ucl': 147.6},
                     9: {'lcl': 149.5, 'std': 154.5, 'ucl': 159.5},
                     10: {'lcl': 161.4, 'std': 166.4, 'ucl': 171.4},
                     11: {'lcl': 174.7, 'std': 176.7, 'ucl': 181.7},
                     12: {'lcl': 215.2, 'std': 215.2, 'ucl': 215.2}},
          'Line2': {1: {'lcl': 45.1, 'std': 50.1, 'ucl': 55.1},
                    2: {'lcl': 67.9, 'std': 72.9, 'ucl': 77.9},
                    3: {'lcl': 88.7, 'std': 93.7, 'ucl': 98.7},
                    4: {'lcl': 106.7, 'std': 111.7, 'ucl': 116.7},
                    5: {'lcl': 122.2, 'std': 127.2, 'ucl': 132.2},
                    6: {'lcl': 136.9, 'std': 141.9, 'ucl': 146.3},
                    7: {'lcl': 150.9, 'std': 155.9, 'ucl': 160.9},
                    8: {'lcl': 163.4, 'std': 168.4, 'ucl': 173.4},
                    9: {'lcl': 175.4, 'std': 180.4, 'ucl': 185.4},
                    10: {'lcl': 188.0, 'std': 193.0, 'ucl': 198.0},
                    11: {'lcl': 201.3, 'std': 206.3, 'ucl': 211.3},
                    12: {'lcl': 213.0, 'std': 218.0, 'ucl': 223.0}},
          'Line3': {1: {'lcl': 46.0, 'std': 51.0, 'ucl': 56.0},
                    2: {'lcl': 67.4, 'std': 72.4, 'ucl': 77.4},
                    3: {'lcl': 87.3, 'std': 92.3, 'ucl': 97.3},
                    4: {'lcl': 105.2, 'std': 110.2, 'ucl': 115.2},
                    5: {'lcl': 121.3, 'std': 126.3, 'ucl': 131.3},
                    6: {'lcl': 136.0, 'std': 141.0, 'ucl': 146.0},
                    7: {'lcl': 149.8, 'std': 154.8, 'ucl': 159.8},
                    8: {'lcl': 162.4, 'std': 167.4, 'ucl': 172.4},
                    9: {'lcl': 174.1, 'std': 179.1, 'ucl': 184.1},
                    10: {'lcl': 187.0, 'std': 192.0, 'ucl': 197.0},
                    11: {'lcl': 200.5, 'std': 205.5, 'ucl': 210.5},
                    12: {'lcl': 212.3, 'std': 217.3, 'ucl': 222.3}},
          'Line4': {1: {'lcl': 41.0, 'std': 46.0, 'ucl': 51.0},
                    2: {'lcl': 62.7, 'std': 67.7, 'ucl': 72.7},
                    3: {'lcl': 83.9, 'std': 88.9, 'ucl': 93.9},
                    4: {'lcl': 103.4, 'std': 108.4, 'ucl': 113.4},
                    5: {'lcl': 120.5, 'std': 125.5, 'ucl': 130.5},
                    6: {'lcl': 135.9, 'std': 140.9, 'ucl': 145.9},
                    7: {'lcl': 149.9, 'std': 154.9, 'ucl': 159.9},
                    8: {'lcl': 162.3, 'std': 167.3, 'ucl': 172.3},
                    9: {'lcl': 174.0, 'std': 179.0, 'ucl': 184.0},
                    10: {'lcl': 187.1, 'std': 192.1, 'ucl': 197.1},
                    11: {'lcl': 201.1, 'std': 206.1, 'ucl': 211.1},
                    12: {'lcl': 212.5, 'std': 217.5, 'ucl': 222.5}},
          'Line5': {1: {'lcl': 41.2, 'std': 46.2, 'ucl': 51.2},
                    2: {'lcl': 62.9, 'std': 67.9, 'ucl': 72.9},
                    3: {'lcl': 83.8, 'std': 88.8, 'ucl': 93.8},
                    4: {'lcl': 102.6, 'std': 107.6, 'ucl': 112.6},
                    5: {'lcl': 119.1, 'std': 124.1, 'ucl': 129.1},
                    6: {'lcl': 134.1, 'std': 139.1, 'ucl': 144.1},
                    7: {'lcl': 147.6, 'std': 152.6, 'ucl': 157.6},
                    8: {'lcl': 160.4, 'std': 165.4, 'ucl': 170.4},
                    9: {'lcl': 172.8, 'std': 177.8, 'ucl': 182.8},
                    10: {'lcl': 186.0, 'std': 191.0, 'ucl': 196.0},
                    11: {'lcl': 199.6, 'std': 204.6, 'ucl': 209.6},
                    12: {'lcl': 210.9, 'std': 215.9, 'ucl': 220.9}},
          'Line6': {1: {'lcl': 44.0, 'std': 49.0, 'ucl': 54.0},
                    2: {'lcl': 65.1, 'std': 70.1, 'ucl': 75.1},
                    3: {'lcl': 86.0, 'std': 91.0, 'ucl': 96.0},
                    4: {'lcl': 105.0, 'std': 110.0, 'ucl': 115.0},
                    5: {'lcl': 122.0, 'std': 127.0, 'ucl': 132.0},
                    6: {'lcl': 137.0, 'std': 142.0, 'ucl': 147.0},
                    7: {'lcl': 151.0, 'std': 156.0, 'ucl': 161.0},
                    8: {'lcl': 163.6, 'std': 168.6, 'ucl': 173.6},
                    9: {'lcl': 175.0, 'std': 180.0, 'ucl': 185.0},
                    10: {'lcl': 187.2, 'std': 192.2, 'ucl': 197.2},
                    11: {'lcl': 200.5, 'std': 205.5, 'ucl': 210.5},
                    12: {'lcl': 210.4, 'std': 215.4, 'ucl': 220.4}},
          'Line7': {1: {'lcl': 41.8, 'std': 46.8, 'ucl': 51.8},
                    2: {'lcl': 61.5, 'std': 66.5, 'ucl': 71.5},
                    3: {'lcl': 83.4, 'std': 88.4, 'ucl': 93.4},
                    4: {'lcl': 103.4, 'std': 108.4, 'ucl': 113.4},
                    5: {'lcl': 120.5, 'std': 125.5, 'ucl': 130.5},
                    6: {'lcl': 135.8, 'std': 140.8, 'ucl': 145.8},
                    7: {'lcl': 150.0, 'std': 155.0, 'ucl': 160.0},
                    8: {'lcl': 162.3, 'std': 167.3, 'ucl': 172.3},
                    9: {'lcl': 173.9, 'std': 178.9, 'ucl': 183.9},
                    10: {'lcl': 186.5, 'std': 191.5, 'ucl': 196.5},
                    11: {'lcl': 200.1, 'std': 205.1, 'ucl': 210.1},
                    12: {'lcl': 211.7, 'std': 216.7, 'ucl': 221.7}},
          'Line8': {1: {'lcl': 43.3, 'std': 48.3, 'ucl': 53.3},
                    2: {'lcl': 65.3, 'std': 70.3, 'ucl': 75.3},
                    3: {'lcl': 86.3, 'std': 91.3, 'ucl': 96.3},
                    4: {'lcl': 105.4, 'std': 110.4, 'ucl': 115.4},
                    5: {'lcl': 121.8, 'std': 126.8, 'ucl': 131.8},
                    6: {'lcl': 137.0, 'std': 142.0, 'ucl': 147.0},
                    7: {'lcl': 150.9, 'std': 155.9, 'ucl': 160.9},
                    8: {'lcl': 163.2, 'std': 168.2, 'ucl': 173.2},
                    9: {'lcl': 175.2, 'std': 180.2, 'ucl': 185.2},
                    10: {'lcl': 188.2, 'std': 193.2, 'ucl': 198.2},
                    11: {'lcl': 201.1, 'std': 206.1, 'ucl': 211.1},
                    12: {'lcl': 212.6, 'std': 217.6, 'ucl': 222.6}},
          'Line9': {1: {'lcl': 35.8, 'std': 40.8, 'ucl': 45.8},
                    2: {'lcl': 55.0, 'std': 60.0, 'ucl': 65.0},
                    3: {'lcl': 77.0, 'std': 82.0, 'ucl': 87.0},
                    4: {'lcl': 96.4, 'std': 101.4, 'ucl': 106.4},
                    5: {'lcl': 114.1, 'std': 119.1, 'ucl': 124.1},
                    6: {'lcl': 130.5, 'std': 135.5, 'ucl': 140.5},
                    7: {'lcl': 145.7, 'std': 150.7, 'ucl': 155.7},
                    8: {'lcl': 162.5, 'std': 167.5, 'ucl': 172.5},
                    9: {'lcl': 182.4, 'std': 187.4, 'ucl': 192.4}}},
 'speed': {'Line1': {'lcl': 98.0, 'ucl': 102.0},
           'Line10': {'lcl': 118.0, 'ucl': 122.0},
           'Line2': {'lcl': 98.0, 'ucl': 102.0},
           'Line3': {'lcl': 98.0, 'ucl': 102.0},
           'Line4': {'lcl': 98.0, 'ucl': 102.0},
           'Line5': {'lcl': 98.0, 'ucl': 102.0},
           'Line6': {'lcl': 98.0, 'ucl': 102.0},
           'Line7': {'lcl': 98.0, 'ucl': 102.0},
           'Line8': {'lcl': 98.0, 'ucl': 102.0},
           'Line9': {'lcl': 78.0, 'ucl': 82.0}}}

DATA_CACHE = []
LAST_REFRESH = None


def nums(text):
    """Extract all numeric values from one line."""
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', text or '')]


def find_line(lines, keyword):
    """Find first line that starts with keyword."""
    for line in lines:
        if line.strip().startswith(keyword):
            return line.strip()
    return ""


def parse_profile(file_path, line_name):
    """Parse one reflow txt profile file."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        start_line = find_line(lines, "Profile Start Time:")
        if not start_line:
            return []

        date_txt = start_line.replace("Profile Start Time:", "").strip()
        dt = datetime.strptime(date_txt, "%a %b %d %H:%M:%S %Y")

        air_l = nums(find_line(lines, "Air Left"))
        air_m = nums(find_line(lines, "Air Middle"))
        air_r = nums(find_line(lines, "Air Right"))

        mass_l = nums(find_line(lines, "Mass Left"))
        mass_m = nums(find_line(lines, "Mass Middle"))
        mass_r = nums(find_line(lines, "Mass Right"))

        # Prefer measured speed; fallback to recipe speed if measured is not available.
        speed_line = find_line(lines, "Measured Conveyor Speed")
        if not speed_line:
            speed_line = find_line(lines, "Conveyor Speed:")

        speed = None
        speed_nums = nums(speed_line)
        if speed_nums:
            speed = speed_nums[0]

        rows = []
        for z in range(12):
            air = None
            mass = None

            if len(air_l) > z and len(air_m) > z and len(air_r) > z:
                air = round((air_l[z] + air_m[z] + air_r[z]) / 3, 2)

            if len(mass_l) > z and len(mass_m) > z and len(mass_r) > z:
                mass = round((mass_l[z] + mass_m[z] + mass_r[z]) / 3, 2)

            rows.append({
                "date": dt.strftime("%Y-%m-%d"),
                "label": dt.strftime("%b %d"),
                "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
                "line": line_name,
                "zone": z + 1,
                "air": air,
                "mass": mass,
                "speed": speed,
                "file": os.path.basename(file_path)
            })

        return rows

    except Exception as e:
        print("Parse error:", file_path, e)
        return []


def load_data():
    """Load all txt files from SRA LINE1-10."""
    all_rows = []

    for i in range(1, 11):
        line_name = f"Line{i}"
        folder = os.path.join(ROOT_FOLDER, f"SRA LINE{i}")
        files = glob.glob(os.path.join(folder, "*.txt"))

        for file_path in files:
            all_rows.extend(parse_profile(file_path, line_name))

    all_rows.sort(key=lambda r: (r["line"], r["datetime"], r["zone"], r["file"]))
    return all_rows


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/refresh")
def refresh():

    global DATA_CACHE, LAST_REFRESH

    DATA_CACHE = load_data()

    import json

    with open(
        "static/data.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            DATA_CACHE,
            f,
            ensure_ascii=False
    )

    with open(
       "static/spec.json",
       "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            SPEC_CACHE,
            f,
            ensure_ascii=False
    )

    LAST_REFRESH = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return jsonify({
        "rows": len(DATA_CACHE),
        "last_refresh": LAST_REFRESH
    })


@app.route("/api/data")
def api_data():
    return jsonify({
        "data": DATA_CACHE,
        "spec": SPEC_CACHE,
        "last_refresh": LAST_REFRESH
    })


if __name__ == "__main__":
    DATA_CACHE = load_data()

    LAST_REFRESH = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )


