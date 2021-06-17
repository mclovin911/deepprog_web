from os.path import abspath
from os.path import split
from os.path import isdir
from simdeep.simdeep_boosting import SimDeepBoosting


def test_instance():
    """
    example of SimDeepBoosting
    """
    PATH_DATA = '{0}/../examples/data/'.format(split(abspath(__file__))[0])

    #Input file
    TRAINING_TSV = {'RNA': 'rna_dummy.tsv', 'METH': 'meth_dummy.tsv'}
    SURVIVAL_TSV = 'survival_dummy.tsv'

    PROJECT_NAME = 'Step1'
    EPOCHS = 10
    SEED = 3
    nb_it = 5
    nb_threads = 2

    # Optional metadata FILE
    OPTIONAL_METADATA = "metadata_dummy.tsv"

    # Import cluster scheduler
    import ray
    ray.init(num_cpus=3)
    # More options can be used (e.g. remote clusters, AWS, memory,...etc...)
    # ray can be used locally to maximize the use of CPUs on the local machine
    # See ray API: https://ray.readthedocs.io/en/latest/index.html

    boosting = SimDeepBoosting(
        nb_threads=nb_threads,
        nb_it=nb_it,
        split_n_fold=3,
        survival_tsv=SURVIVAL_TSV,
        training_tsv=TRAINING_TSV,
        path_data=PATH_DATA,
        project_name=PROJECT_NAME,
        path_results=PATH_DATA,
        metadata_tsv=OPTIONAL_METADATA, # optional
        use_r_packages=False, # to use R functions from the survival and survcomp packages
        metadata_usage='all',
        epochs=EPOCHS,
        distribute=True, # Option to use ray cluster scheduler
        seed=SEED)

    boosting.fit()
    boosting.save_models_classes()
    
    # Close clusters and free memory
    ray.shutdown()


if __name__ == '__main__':
    test_instance()