from typing import Union, Optional

from maa.context import Context
from maa.custom_recognition import CustomRecognition
from maa.define import RectType


class MyRecognizer(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> Union[CustomRecognition.AnalyzeResult, Optional[RectType]]:


        print("成功注册MyRecognizer")
        return None
    
