"""

Partitions an assignment into zip folders

Usage:
python zip_assignment.py <assign_num> <num_paritions>

"""

import sys
from utils.file_utils import partition_assignment


if __name__ == "__main__":
	assign_num = int(sys.argv[1])
	num_partitions = int(sys.argv[2])
	partition_assignment(assign_num, num_partitions)
