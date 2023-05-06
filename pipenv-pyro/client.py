from Pyro5.api import Proxy, config, register_dict_to_class, register_class_to_dict
import mycustomclasses




# register the special serialization hooks

def thingy_class_to_dict(obj):
    print("{serializer hook, converting to dict: %s}" % obj)
    return {
        "__class__": "waheeee-custom-thingy",
        "number-attribute": obj.number
    }


def thingy_dict_to_class(classname, d):
    print("{deserializer hook, converting to class: %s}" % d)
    return mycustomclasses.Thingy(d["number-attribute"])


# for 'Thingy' we register both serialization and deserialization hooks
register_dict_to_class("waheeee-custom-thingy", thingy_dict_to_class)
register_class_to_dict(mycustomclasses.Thingy, thingy_class_to_dict)


# regular pyro stuff
uri = input("Enter the URI of the server object: ")
serv = Proxy(uri)
print("\nTransferring thingy...")
o = mycustomclasses.Thingy(42)
response = serv.method(o)
print("type of response object:", type(response))
print("response:", response)
