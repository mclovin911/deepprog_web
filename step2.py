from os.path import abspath
from os.path import split
from os.path import isdir

from simdeep.simdeep_boosting import SimDeepBoosting


def test_instance(Omic, test_name):
    """
    example of SimDeepBoosting starting from precomputed labels
    To obtain precomputed label files that can be used as an example, please run
    the `example_with_dummy_data.py` example script
    """
    cancer = 'COAD'
    PATH_PRECOMPUTED_LABELS = '//home/ubuntu/data/DeepProg/matrices/{0}/{0}/saved_models_classes'.format(cancer)

    if not isdir(PATH_PRECOMPUTED_LABELS):
        print('No folder: {0} found' \
              ' Please run {1}/example_with_dummy_data.py script'.format(
                  PATH_PRECOMPUTED_LABELS, split(abspath(__file__))[0]))
        return

    PATH_DATA = '//home/ubuntu/data/DeepProg/matrices/{0}'.format(cancer)

    #Input file
    rna_file = 'rna_mapped_{0}.tsv'.format(cancer)
    meth_file = 'meth_mapped_{0}.tsv'.format(cancer)
    mir_file = 'mir_mapped_{0}.tsv'.format(cancer)
    survival_file = 'surv_mapped_{0}.tsv'.format(cancer)

    TRAINING_TSV = {'RNA': rna_file, 'METH': meth_file, 'MIR': mir_file}
    SURVIVAL_TSV = survival_file 

    PROJECT_NAME = 'Step2_{0}'.format(cancer)
    # SEED = 3
    nb_it = 5 # Number of models to be built
    nb_threads = 2 # Number of processes to be used to fit individual survival models

    # Import distributed modules
    import ray
    ray.init(num_cpus=3)

    boosting = SimDeepBoosting(
        nb_threads=nb_threads,
        nb_it=nb_it,
        split_n_fold=3,
        survival_tsv=SURVIVAL_TSV,
        training_tsv=TRAINING_TSV,
        path_data=PATH_DATA,
        project_name=PROJECT_NAME,
        path_results=PATH_DATA,
        distribute=True, # Option to use ray cluster scheduler (OPTIONAL)
    )

    boosting.fit_on_pretrained_label_file(
        labels_files_folder=PATH_PRECOMPUTED_LABELS,
        file_name_regex="*.tsv")
    boosting.predict_labels_on_full_dataset()

    boosting.compute_clusters_consistency_for_full_labels()
    boosting.evalutate_cluster_performance()
    boosting.collect_cindex_for_test_fold()
    boosting.collect_cindex_for_full_dataset()

    boosting.compute_feature_scores_per_cluster()
    boosting.write_feature_score_per_cluster()
    boosting.collect_number_of_features_per_omic()
    boosting.compute_pvalue_for_merged_test_fold()

    boosting.load_new_test_dataset(
        #{'RNA': Omic}, # OMIC file of the test set. It doesnt have to be the same as for training
        Omic,
        test_name # Name of the test test to be used
    )

    boosting.predict_labels_on_test_dataset()

    # boosting.compute_c_indexes_for_test_dataset()
    # boosting.compute_clusters_consistency_for_test_labels()

    ray.shutdown()

if __name__ == '__main__':
    test_instance( {'METH': '../../../../code/DeepProg/examples/data/meth_dummy.tsv'}, 'step2_test')

