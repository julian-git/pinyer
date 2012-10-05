import pstats

if __name__ == '__main__':
    p = pstats.Stats('xml_to_svg.stats')
    p.sort_stats('time', 'cum').print_stats(15)
#    p.sort_stats('cumulative').print_stats(15)
