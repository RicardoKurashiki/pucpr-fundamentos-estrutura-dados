from utils import generate_data

def linear_array_test(data):
    pass

def tree_test(data):
    pass

def hash_test(data):
    pass

def main():    
    data = generate_data(50_000)
    linear_array_test(data)
    tree_test(data)
    hash_test(data)

if __name__ == "__main__":
    main()