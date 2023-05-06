from Pyro5.api import expose, serve, config, register_class_to_dict, register_dict_to_class
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


# regular Pyro server stuff

@expose
class Server(object):
    def method(self, arg):
        print("\nmethod called, arg=", arg)
        response = mycustomclasses.Thingy(999)
        return response


serve({Server: "example.customclasses"}, use_ns=False)
