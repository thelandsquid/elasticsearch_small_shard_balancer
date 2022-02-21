from config.FileSizeDict import FileSizeDict

def print_largest_indices(datastore, limit=None):
    fsd, i = FileSizeDict(), 0
    print("LARGEST INDICES")
    print("{:<50} {:<20}".format("Index","Size"))
    for index in sorted(datastore.indices_dict.values(),key=lambda x:x.get_disk_size(), reverse=True):   
        print("{:<50} {:<20}".format(index.name, fsd.size_to_text(index.disk_size)))
        i+=1
        if(i is not None and i>=limit):
            break