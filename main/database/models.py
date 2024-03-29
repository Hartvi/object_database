from django.db import models
from django.db.models import QuerySet
# from django.db.backends import base.Query
from rest_framework import serializers


"""
class MyManager:
    def filter(self, *args, **kwargs) -> QuerySet:
        pass

    def all(self, *args, **kwargs) -> QuerySet:
        pass


class MyBaseModel(models.Model):
    objects = MyManager()
    # objects = models.manager.Manager()

    class Meta:
        abstract = True
"""


class Quantity(models.Model):
    name = models.CharField(max_length=100, unique=True)


class ObjectInstance(models.Model):
    is_instance = models.BooleanField(default=True)
    local_instance_id = models.IntegerField(null=True)
    # global_instance_id = models.IntegerField(null=True, unique=True)  # this can be replaced by a probabilistic blockchain
    dataset = models.CharField(max_length=100, null=True)
    dataset_id = models.CharField(max_length=100, null=True)
    maker = models.CharField(max_length=100, null=True)
    common_name = models.CharField(max_length=100, null=True)
    other = models.JSONField(null=True)
    other_file = models.FileField(null=True)
    has_image = models.BooleanField(default=False, null=True)
    is_the_same_as = models.ForeignKey("ObjectInstance",
                                       on_delete=models.PROTECT,
                                       related_name="object_instances",
                                       null=True)

    owner = models.ForeignKey('accounts.CustomUser',
                              on_delete=models.CASCADE,
                              related_name='object_instances',
                              null=True)


class Setup(models.Model):
    """
    {"arm": "arm_name", "gripper": "gripper_name", "camera": "camera_model_name",
     "microphone": "microphone_model_name"}
    """
    created = models.DateTimeField(auto_now_add=True)


class SetupElement(models.Model):
    # this could be from the choices: arm, gripper, camera, depth, camera, microphone, other
    type = models.CharField(max_length=100, )
    name = models.CharField(max_length=100, unique=True)
    output_quantities = models.JSONField(null=True)  # e.g. time, position, current, force, rgb, depth, bw (as in black & white)
    parameters = models.JSONField(null=True)
    setup = models.ManyToManyField(Setup, related_name='setup_elements')
    quantities = models.ManyToManyField(Quantity, related_name='setup_elements')

    # def __str__(self):
    #     return str(self.type) + ", " + str(self.name)


class Measurement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    png = models.ImageField()  # upload_to='measurements/'
    setup = models.ForeignKey(Setup, related_name='measurements', related_query_name='measurement',
                              on_delete=models.CASCADE, null=True)
    object_instance = models.ForeignKey(ObjectInstance,
                                        on_delete=models.CASCADE, related_name='measurements', null=True)
    owner = models.ForeignKey('accounts.CustomUser', related_name='measurements', related_query_name='measurement',
                              on_delete=models.PROTECT, null=True)
    consider_this_ground_truth = models.BooleanField(default=False, null=True)
    method = models.CharField(max_length=100, null=True)
    quantities = models.ManyToManyField(Quantity, related_name='measurements')

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        # print("saving measurement:", args, kwargs)
        super().save(*args, **kwargs)


class SensorOutput(models.Model):
    sensor_output_file = models.FileField(null=True)  # , upload_to="outputs/"
    sensor_output = models.JSONField(null=True)
    sensor_output_large = models.FileField(null=True)
    sensor = models.ForeignKey(SetupElement, on_delete=models.CASCADE, related_name='sensor_outputs', )
    parameters = models.JSONField(null=True)  # something like sensor input - sensor parameters during the measurement
    measurements = models.ForeignKey(Measurement, related_name='sensor_outputs', on_delete=models.CASCADE, null=True)


class Pose(models.Model):
    rx = models.FloatField(default=0)
    ry = models.FloatField(default=0)
    rz = models.FloatField(default=0)
    tx = models.FloatField(default=0)
    ty = models.FloatField(default=0)
    tz = models.FloatField(default=0)

    class Meta:
        abstract = True


class GraspProposal(Pose):
    number_of_fingers = models.IntegerField(default=2)
    gripper = models.CharField(max_length=100, null=True)
    gripper_object = models.ForeignKey(SetupElement, on_delete=models.CASCADE, null=True)
    source = models.CharField(max_length=100)  # how it was generated
    parameters = models.JSONField(default=dict)
    object_instance = models.ForeignKey(ObjectInstance, related_name='grasp_proposal', on_delete=models.CASCADE, null=False)
    successful_measurement = models.OneToOneField(Measurement, related_name='grasp_proposal', on_delete=models.CASCADE, null=True)


class Grasp(Pose):

    grasped = models.BooleanField(null=True)
    measurement = models.OneToOneField(Measurement, related_name='grasp', on_delete=models.CASCADE, null=True)


class GripperPose(Pose):

    grasped = models.BooleanField(null=True)
    measurement = models.OneToOneField(Measurement, related_name='gripper_pose', on_delete=models.CASCADE, null=True)


class ObjectPose(Pose):

    measurement = models.OneToOneField(Measurement, related_name='object_pose', on_delete=models.CASCADE, null=True)


class Entry(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    measurement = models.ForeignKey(Measurement, related_name='entries', related_query_name='entry',
                                    on_delete=models.CASCADE, null=True)
    repository = models.URLField(null=True, default='http://www.github.com')  # link to repository
    owner = models.ForeignKey('accounts.CustomUser', related_name='entries', related_query_name='entry',
                              on_delete=models.PROTECT, null=True)
    type = models.CharField(max_length=100, null=True)  # categorical => ignore std's, continuous, others
    name = models.CharField(max_length=100, null=True)  # e.g. {"type": "continuous", "name": "size"}
    ground_truth = models.BooleanField(null=True, default=False)  # e.g. measured with a professional setup
    object_instance = models.ForeignKey(ObjectInstance,
                                        on_delete=models.CASCADE, related_name='entries', null=True)
    setup_element = models.ForeignKey(SetupElement, on_delete=models.CASCADE, related_name='entries', null=True)
    sensor_output = models.ForeignKey(SensorOutput, on_delete=models.CASCADE, related_name='entries', null=True)
    quantities = models.ManyToManyField(Quantity, related_name='entries')

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        # print("saving entry:", args, kwargs)
        # exit(1)
        super().save(*args, **kwargs)


class PropertyElement(models.Model):  # this should, I think, be possible to bind only in a OneToOneField
    name = models.CharField(max_length=100)
    value = models.FloatField(null=True)
    std = models.FloatField(null=True)
    units = models.CharField(max_length=100)
    other = models.JSONField(null=True)  # for friction, etc.
    other_file = models.FileField(null=True)  # , upload_to="properties/"
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='property_element')


class OutputQuantity(models.Model):
    name = models.CharField(max_length=100)


class ObjectImage(models.Model):
    # WARNING: this might have to have the media prefix added to it: /ipalm/media/ or /media/
    img = models.FileField(null=True)  # set with object_image.img.name = existing_name and then object_image.save()
    # source_field = models.ForeignKey(models.Model,
    #                                     on_delete=models.CASCADE, related_name='object_images', null=True)
    object_instance = models.ForeignKey(ObjectInstance,
                                        on_delete=models.CASCADE, related_name='object_images', null=True)


# class InputQuantity(models.Model):  # this is basically the setup elements

