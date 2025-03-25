import os
import sys
from maa.agent.agent_server import AgentServer
from maa.toolkit import Toolkit
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition


def load_custom_objects(agent, custom_dir):
    if not os.path.exists(custom_dir):
        print(f"自定义文件夹 {custom_dir} 不存在")
        return

    if not os.listdir(custom_dir):
        print(f"自定义文件夹 {custom_dir} 为空")
        return

    # Save original path
    original_path = sys.path.copy()
    
    # Process module types
    for module_type, base_class in [("custom_actions", CustomAction),
                                   ("custom_recognition", CustomRecognition)]:
        module_type_dir = os.path.join(custom_dir, module_type)

        if not os.path.exists(module_type_dir):
            print(f"{module_type} 文件夹不存在于 {custom_dir}")
            continue

        print(f"开始加载 {module_type} 模块")
        
        # Add module directory to path to enable imports
        sys.path.insert(0, module_type_dir)
        
        for file in os.listdir(module_type_dir):
            file_path = os.path.join(module_type_dir, file)
            
            if os.path.isfile(file_path) and file.endswith('.py'):
                try:
                    module_name = os.path.splitext(file)[0]
                    
                    # Import the module
                    module = __import__(module_name)
                    
                    # Find all classes in module that are subclasses of the base class
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        if isinstance(attr, type) and issubclass(attr, base_class) and attr != base_class:
                            class_name = attr.__name__
                            instance = attr()
                            
                            if module_type == "custom_actions":
                                if agent.register_custom_action(class_name, instance):
                                    print(f"加载自定义动作 {class_name} 成功")
                            elif module_type == "custom_recognition":
                                if agent.register_custom_recognition(class_name, instance):
                                    print(f"加载自定义识别器 {class_name} 成功")
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    
        # Restore path
        sys.path = original_path


def main():
    Toolkit.init_option("./")

    # socket_id = sys.argv[-1]
    socket_id = "111-222-333-444"

    load_custom_objects(AgentServer, "./yys_base/custom_dir")
    print("当前socket_id:", socket_id)
    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()


if __name__ == "__main__":
    main()