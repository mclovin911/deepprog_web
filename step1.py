from os.path import abspath
from os.path import split
from os.path import isdir
from simdeep.simdeep_boosting import SimDeepBoosting


def test_instance():
    """
    example of SimDeepBoosting
    """
    cancer = 'COAD'

    PATH_DATA = '//home/ubuntu/data/DeepProg/matrices/{0}'.format(cancer)

    #Input file

    rna_file = 'rna_mapped_{0}.tsv'.format(cancer)
    meth_file = 'meth_mapped_{0}.tsv'.format(cancer)
    mir_file =e = 'surv_mapped_{0}.tsv'.format(cancer)

    TRAINING_TSV = 'mir_mapped_{0}.tsv'.format(cancer)
    survival_fil {'RNA': rna_file, 'METH': meth_file, 'MIR': mir_file}
    SURVIVAL_TSV = survival_file

    PROJECT_NAME = cancer
    EPOCHS = 10
    SEED = 3
    nb_it = 5
    nb_threads = 2

    # Optional metadata FILE
    OPTIONAL_METADATA = None

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