#!/usr/bin/env python3
from glob import glob
from string import Template
from subprocess import check_output,PIPE,Popen
import argparse
CONFIG = Template('''{
    "ContactNetwork":                                  "NetworkX",

    "ContactNetworkGenerator":                         "BarabasiAlbert",
    "num_cn_nodes":                                    100000,
    "num_edges_from_new":                              2,

    "Driver":                                          "Default",
    "out_dir":                                         "${containing_dir}/CLUSTERS_${clusters}_REP_${rep}",

    "EndCriteria":                                     "GEMF",
    "gemf_path":                                       "GEMF",

    "Logging":                                         "File",

    "NodeAvailability":                                "Perfect",

    "NodeEvolution":                                   "VirusTreeSimulator",
    "java_path":                                       "java",
    "nw_rename_path":                                  "nw_rename",
    "vts_growthRate":                                  2.851904, # per year (PANGEA)
    "vts_model":                                       "logistic",
    "vts_n0":                                          1,
    "vts_t50":                                         -2, # years (PANGEA)

    "NumBranchSample":                                 "Single",

    "NumTimeSample":                                   "Once",

    "PostValidation":                                  "Dummy",

    "SeedSelection":                                   "Random",
    "num_seeds":                                       ${clusters},

    "SeedSequence":                                    "VirusMeanCoalescentGTRGamma",
    "hmmemit_path":                                    "hmmemit",
    "seed_tree_height":                                5, # years
    "seqgen_path":                                     "seq-gen",
    "seqgen_a_to_c":                                   1.765707,
    "seqgen_a_to_g":                                   9.587649,
    "seqgen_a_to_t":                                   0.691915,
    "seqgen_c_to_g":                                   0.863348,
    "seqgen_c_to_t":                                   10.282617,
    "seqgen_g_to_t":                                   1.000000,
    "seqgen_freq_a":                                   0.392,
    "seqgen_freq_c":                                   0.165,
    "seqgen_freq_g":                                   0.212,
    "seqgen_freq_t":                                   0.232,
    "seqgen_gamma_shape":                              0.405129,
    "seqgen_num_gamma_rate_categories":                "",
    "viral_sequence_type":                             "HIV1-B-DNA-POL-LITTLE",

    "SequenceEvolution":                               "GTRGammaSeqGen",

    "Sequencing":                                      "GrinderSanger",
    "grinder_path":                                    "grinder",

    "SourceSample":                                    "Random",

    "TimeSample":                                      "GranichFirstART",

    "TransmissionNodeSample":                          "GEMF",

    "TransmissionTimeSample":                          "HIVARTGranichGEMF",
    "end_time":                                        15, # years
    "hiv_a1_to_a2":                                    52./12.,
    "hiv_a1_to_d":                                     0,
    "hiv_a1_to_i1":                                    12./25.,
    "hiv_a2_to_a3":                                    0,
    "hiv_a2_to_d":                                     0,
    "hiv_a2_to_i2":                                    12./25.,
    "hiv_a3_to_a4":                                    0,
    "hiv_a3_to_d":                                     0,
    "hiv_a3_to_i3":                                    0,
    "hiv_a4_to_d":                                     0,
    "hiv_a4_to_i4":                                    0,
    "hiv_i1_to_a1":                                    365./365.,
    "hiv_i1_to_d":                                     0,
    "hiv_i1_to_i2":                                    52./6.,
    "hiv_i2_to_a2":                                    365./365.,
    "hiv_i2_to_d":                                     0,
    "hiv_i2_to_i3":                                    0,
    "hiv_i3_to_a3":                                    0,
    "hiv_i3_to_d":                                     0,
    "hiv_i3_to_i4":                                    0,
    "hiv_i4_to_a4":                                    0,
    "hiv_i4_to_d":                                     0,
    "hiv_ns_to_d":                                     0,
    "hiv_ns_to_s":                                     999999,
    "hiv_s_to_d":                                      0,
    "hiv_s_to_i1_by_a1":                               0.0225,
    "hiv_s_to_i1_by_a2":                               0,
    "hiv_s_to_i1_by_a3":                               0,
    "hiv_s_to_i1_by_a4":                               0,
    "hiv_s_to_i1_by_i1":                               0.45,
    "hiv_s_to_i1_by_i2":                               0.09,
    "hiv_s_to_i1_by_i3":                               0,
    "hiv_s_to_i1_by_i4":                               0,
    "hiv_s_to_i1_seed":                                0, # 0.05*0.09, # 5% of rate from I2

    "TreeNode":                                        "Simple",

    "TreeUnit":                                        "LogNormal",
    "tree_rate_mean":                                  -8, #-6.164298, # per year (PANGEA)
    "tree_rate_stdev":                                 0.3, # per year (PANGEA)
}
''')

# parse user args
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-c', '--clusters', required=True, type=int, help="Number of Clusters (Seeds)")
parser.add_argument('-r', '--rep', required=True, type=int, help="Replicate Number")
parser.add_argument('-f', '--favites', required=False, type=str, default="/scratchfast/a1moshir/bin/FAVITES/run_favites.py", help="Path to FAVITES executable")
args = parser.parse_args()

# create config file
config_file = 'clusters_%d_rep_%d.json' % (args.clusters, args.rep)
f = open(config_file, 'w')
f.write(CONFIG.substitute(clusters=args.clusters, rep=args.rep, containing_dir="FAVITES_output"))
f.close()

# run FAVITES
check_output([args.favites,'-c',config_file])

# merge sequences into single FASTA file
rep_folder = "CLUSTERS_%d_REP_%d" % (args.clusters,args.rep)
sequence_data_dir = "FAVITES_sequence_output/%s" % rep_folder
check_output(['mkdir',sequence_data_dir])
p = Popen("fastq_merge.py FAVITES_output/%s/error_prone_files/sequence_data/*.fastq | fastq2fasta.py > %s/%s.fas" % (rep_folder,sequence_data_dir,rep_folder), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.communicate()

# run MAFFT
p = Popen("mafft --auto %s/%s.fas > %s/%s.aln" % (sequence_data_dir,rep_folder,sequence_data_dir,rep_folder), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.communicate()

# run FastTree
p = Popen("FastTree -nt -gtr < %s/%s.aln > %s/%s.tre" % (sequence_data_dir,rep_folder,sequence_data_dir,rep_folder), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.communicate()

# run ClusterPicker
check_output(['ClusterPicker_1.2.5.jar', "%s/%s.aln" % (sequence_data_dir,rep_folder), "%s/%s.tre" % (sequence_data_dir,rep_folder), '0.9', '0.9', '0.045', '0'])
p = Popen("~/bin/FAVITES/helper_scripts/cluster_picker_accuracy.py -c %s/%s_clusterPicks_list.txt -t FAVITES_output/%s/error_free_files/transmission_network.txt > %s/%s.accuracy.clusterpicker.txt" % (sequence_data_dir,rep_folder,rep_folder,sequence_data_dir,rep_folder), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
p.communicate()
