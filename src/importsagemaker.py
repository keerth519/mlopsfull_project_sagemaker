import sagemaker
from sagemaker.core import image_uris
import sys
print(image_uris.retrieve(
    framework='sklearn', 
    region = 'ap-southeast-2',
    version = '1.4-2-py312', 
    instance_type = 'ml.t3.medium',
    image_scope = 'inference'
    ))

print (sys.version)

""" errorTraceback (most recent call last):
  File "/workspaces/mlopsfull_project_sagemaker/src/importsagemaker.py", line 2, in <module>
    from sagemaker.image_uris import retrieve
ModuleNotFoundError: No module named 'sagemaker.image_uris' """
# we have chnaged the to '1.4-2-py312' and from sagemaker.core import image_uris  the issue is resolved 