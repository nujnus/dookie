from fire.core import Fire
from cookiecutter.main import cookiecutter
import datetime
import json
import re


class Dookie(object):
    def __init__(self):
        pass

    def run(self, template):

        pattern = r"(\w+)\@(\w+)"
        custom_filters = {}

        def dookie_format(value):
            '''
            自定义filter函数: 
            根据pattern,
            返回group(2)对应的另一个filter函数,
            并以group(1)作为其参数, 就像是写在后面的装饰器.
            '''
            result = re.match(pattern, value)

            if result:
                return custom_filters[result.group(2)](result.group(1))
            else:
                return value

        def ToPascalCase(value):
            '''
            自定义filter函数: 
            从 snake_case, camelCase, kebab-case
            转换成PascalCase的命名方式.
            '''
            return ''.join(list(map((lambda x: x.capitalize()), value.replace("-", " ").replace("_", " ").split(' '))))

        timestamp = datetime.datetime.now()

        def append_datetime(value):
            '''
            自定义filter函数: 
            在字符串后追加一个全局统一的时间戳.
            '''
            return '{}_{}'.format(value, timestamp.strftime('%Y_%m_%d_%H_%M_%S'))

        def append_hextime(value):
            return '{}_{}'.format(value, hex(int(timestamp.strftime('%y%m%d%H%M%S'))).replace(r'0x', '').upper())

        # 注册filter函数
        custom_filters['ToPascalCase'] = ToPascalCase
        custom_filters['append_datetime'] = append_datetime
        custom_filters['append_hextime'] = append_hextime
        custom_filters['dookie_format'] = dookie_format


        cookiecutter(template, extra_context={'improver_and_developer': 'nujnus'}, custom_filters=custom_filters)


if __name__ == '__main__':
    Fire(Dookie)
