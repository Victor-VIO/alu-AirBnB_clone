#!/usr/bin/python3
"""Console for AirBnB clone"""
import cmd
import shlex
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""
    
    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }
    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True
    
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True
    
    def emptyline(self):
        """Do nothing on empty line"""
        pass
    
    def do_create(self, arg):
        """Create a new instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        
        new_instance = self.__classes[class_name]()
        new_instance.save()
        print(new_instance.id)
    
    def do_show(self, arg):
        """Show string representation of an instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        
        print(storage.all()[key])
    
    def do_destroy(self, arg):
        """Delete an instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        
        del storage.all()[key]
        storage.save()
        print("Instance deleted successfully")
    
    def do_all(self, arg):
        """Print all string representations"""
        args = shlex.split(arg)
        obj_list = []
        
        if args and args[0] not in self.__classes:
            print("** class doesn't exist **")
            return
        
        for key, obj in storage.all().items():
            if not args or (args and key.split('.')[0] == args[0]):
                obj_list.append(str(obj))
        
        print(obj_list)
    
    def do_update(self, arg):
        """Update an instance attribute"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        
        if len(args) < 3:
            print("** attribute name missing **")
            return
        
        if len(args) < 4:
            print("** value missing **")
            return
        
        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]
        
        # Skip if trying to update id, created_at, or updated_at
        if attr_name in ["id", "created_at", "updated_at"]:
            print(f"Cannot update {attr_name}")
            return
        
        # Cast attribute value to appropriate type
        try:
            # Try to convert to int
            if attr_value.isdigit() or (attr_value.startswith('-') and attr_value[1:].isdigit()):
                attr_value = int(attr_value)
            # Try to convert to float
            elif '.' in attr_value and all(part.isdigit() or (part.startswith('-') and part[1:].isdigit()) for part in attr_value.split('.', 1)):
                attr_value = float(attr_value)
            # Remove quotes if present
            elif (attr_value.startswith('"') and attr_value.endswith('"')) or \
                 (attr_value.startswith("'") and attr_value.endswith("'")):
                attr_value = attr_value[1:-1]
        except (ValueError, AttributeError):
            pass  # Keep as string if conversion fails
        
        setattr(obj, attr_name, attr_value)
        obj.save()
        print(f"Updated {class_name} {args[1]} with {attr_name} = {attr_value}")
    
    def default(self, line):
        """Handle class-specific commands like User.all()"""
        parts = line.split('.')
        if len(parts) == 2:
            class_name = parts[0]
            method_call = parts[1]
            
            if class_name in self.__classes:
                if method_call == "all()":
                    self.do_all(class_name)
                elif method_call == "count()":
                    count = sum(1 for key in storage.all().keys() if key.startswith(class_name + '.'))
                    print(count)
                elif method_call.startswith("show(") and method_call.endswith(")"):
                    instance_id = method_call[5:-1].strip('"\'')
                    self.do_show(f"{class_name} {instance_id}")
                elif method_call.startswith("destroy(") and method_call.endswith(")"):
                    instance_id = method_call[8:-1].strip('"\'')
                    self.do_destroy(f"{class_name} {instance_id}")
                return
        
        print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
