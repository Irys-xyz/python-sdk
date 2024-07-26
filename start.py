from tags import encode_tags, decode_tags

if __name__ == '__main__':
    tags = [("hi", "hey")]
    print(decode_tags(encode_tags(tags)))
