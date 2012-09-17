import pstats

if __name__ == '__main__':
    p = pstats.Stats('build_ip.stats')
    p.sort_stats('time').print_stats(15)
#    p.sort_stats('cumulative').print_stats(15)
