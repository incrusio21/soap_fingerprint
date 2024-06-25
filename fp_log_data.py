from scheduler import get_fp_soap

if __name__ == '__main__':
    fp = get_fp_soap()
    if fp:
        fp.get_log_data()