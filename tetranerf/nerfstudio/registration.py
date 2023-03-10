from nerfstudio.data.datamanagers.base_datamanager import VanillaDataManagerConfig
from nerfstudio.data.dataparsers.minimal_dataparser import MinimalDataParserConfig
from nerfstudio.engine.optimizers import RAdamOptimizerConfig
from nerfstudio.engine.schedulers import ExponentialDecaySchedulerConfig
from nerfstudio.engine.trainer import TrainerConfig
from nerfstudio.pipelines.base_pipeline import VanillaPipelineConfig
from nerfstudio.plugins.types import MethodSpecification

from .model import TetrahedraNerf, TetrahedraNerfConfig
from .pipeline import TetrahedraNerfPipeline

tetranerf_config = TrainerConfig(
    method_name="tetra-nerf",
    pipeline=VanillaPipelineConfig(
        _target=TetrahedraNerfPipeline,
        datamanager=VanillaDataManagerConfig(
            # _target=RayPruningDataManager,
            dataparser=MinimalDataParserConfig(),
            eval_num_rays_per_batch=4096,
            train_num_rays_per_batch=4096,
        ),
        model=TetrahedraNerfConfig(_target=TetrahedraNerf),
    ),
    max_num_iterations=300000,
    steps_per_save=25000,
    steps_per_eval_batch=1000,
    steps_per_eval_image=2000,
    steps_per_eval_all_images=50000,
    optimizers={
        "fields": {
            "optimizer": RAdamOptimizerConfig(lr=0.001),
            "scheduler": ExponentialDecaySchedulerConfig(
                lr_final=0.0001,
                max_steps=300_000,
            ),
        },
    },
)


tetranerf = MethodSpecification(config=tetranerf_config, description="Official implementation of Tetra-NeRF paper")
