
def main():
    check_bom('badfile.txt')
    check_bom('goodfile.txt')
    check_bom('bad_in_the_middle.txt')

def check_bom(fname):
    with open(fname, 'r') as f:
        content = f.read()
    bom = '\uFEFF'
    print(fname, 'has BOM?', bom in content) 

if __name__ == '__main__':
    main()
