import unittest
import sys
import argparse

from uncertainpy.tests import *

def create_test_suite(test_classes_to_run):
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    return big_suite


test_distribution = create_test_suite([TestDistribution])
test_evaluateNodeFunction = create_test_suite([TestEvaluateNodeFunction])


test_spike_sorting = create_test_suite([TestSpike, TestSpikes])

test_features = create_test_suite([TestGeneralFeatures,
                                   TestGeneralNeuronFeatures,
                                   TestNeuronFeatures,
                                   TestTestingFeatures])

test_features.addTest(test_spike_sorting)

test_logger = create_test_suite([TestLogger])

test_runModel = create_test_suite([TestRunModel])

test_model = create_test_suite([TestModel,
                                TestHodkinHuxleyModel,
                                TestCoffeeCupPointModel,
                                TestIzhikevichModel,
                                TestTestingModel0d,
                                TestTestingModel1d,
                                TestTestingModel2d,
                                TestTestingModel0dNoTime,
                                TestTestingModel1dNoTime,
                                TestTestingModel2dNoTime,
                                TestTestingModelNoU,
                                TestNeuronModel])
test_model.addTest(test_runModel)

test_parameters = create_test_suite([TestParameter, TestParameters])

test_plotting = create_test_suite([TestPrettyPlot, TestPrettyBar])

test_plotUncertainty = create_test_suite([TestPlotUncertainpy])

test_uncertainty = create_test_suite([TestUncertainty])

test_exploration = create_test_suite([TestExploration])

test_usecase = create_test_suite([TestUseCases])


test_utils = unittest.TestSuite([test_logger, test_plotting])
test_prerequisites = unittest.TestSuite([test_utils,
                                        test_parameters,
                                        test_distribution,
                                        test_features,
                                        test_evaluateNodeFunction,
                                        test_model])



test_basic = unittest.TestSuite([test_prerequisites,
                                test_uncertainty,
                                test_plotUncertainty])

test_fast = unittest.TestSuite([test_basic, test_exploration])

test_all = unittest.TestSuite([test_fast, test_usecase])


test_runner = unittest.TextTestRunner()

parser = argparse.ArgumentParser(description="Run tests for Uncertainpy")
parser.add_argument("-u", "--utils", help="Utility tests", action="store_true")
parser.add_argument("-p", "--prerequisites", help="Prerequisites tests", action="store_true")
parser.add_argument("-a", "--all", help="All tests", action="store_true")
parser.add_argument("-b", "--basic", help="Basic tests (all test up to Uncertainpy)", action="store_true")
parser.add_argument("-f", "--fast", help="Run all tests except usecase test", action="store_true")

parser.add_argument("--uncertainpy", help="Uncertainpy tests", action="store_true")
parser.add_argument("--exploration", help="UncertaintyEstimations (explorations) test", action="store_true")
parser.add_argument("--parameters", help="Parameter tests", action="store_true")
parser.add_argument("--distribution", help="Distribution tests", action="store_true")
parser.add_argument("--evaluatenodefunction", help="evaluatenodefunction tests", action="store_true")
parser.add_argument("--spike_sorting", help="spike_sorting tests", action="store_true")
parser.add_argument("--plotuncertainty", help="PlotUncertainty tests", action="store_true")
parser.add_argument("--features", help="Features tests", action="store_true")
parser.add_argument("--model", help="Model tests", action="store_true")
parser.add_argument("--runmodel", help="RunModel tests", action="store_true")
parser.add_argument("--logger", help="Logger tests", action="store_true")
parser.add_argument("--plotting", help="Plotting tests", action="store_true")
parser.add_argument("--usecase", help="Usecase tests", action="store_true")

args = parser.parse_args()


results = {}

if args.utils:
    print "-----------------------------------------"
    print "Running testsuite: utils"
    results["utils"] = test_runner.run(test_utils)
if args.prerequisites:
    print "-----------------------------------------"
    print "Running testsuite: prerequisites"
    results["prerequisites"] = test_runner.run(test_prerequisites)
if args.all:
    print "-----------------------------------------"
    print "Running testsuite: all"
    results["all"] = test_runner.run(test_all)
if args.basic:
    print "-----------------------------------------"
    print "Running testsuite: basic"
    results["basic"] = test_runner.run(test_basic)
if args.fast:
    print "-----------------------------------------"
    print "Running testsuite: fast"
    results["fast"] = test_runner.run(test_fast)
if args.uncertainpy:
    print "-----------------------------------------"
    print "Running testsuite: uncertainpy"
    results["uncertainpy"] = test_runner.run(test_uncertainty)
if args.exploration:
    print "-----------------------------------------"
    print "Running testsuite: exploration"
    results["exploration"] = test_runner.run(test_exploration)
if args.parameters:
    print "-----------------------------------------"
    print "Running testsuite: parameters"
    results["parameters"] = test_runner.run(test_parameters)
if args.distribution:
    print "-----------------------------------------"
    print "Running testsuite: distribution"
    results["distribution"] = test_runner.run(test_distribution)
if args.evaluatenodefunction:
    print "-----------------------------------------"
    print "Running testsuite: evaluateNodeFunction"
    results["evaluateNodeFunction"] = test_runner.run(test_evaluateNodeFunction)
if args.spike_sorting:
    print "-----------------------------------------"
    print "Running testsuite: spike_sorting"
    results["spike_sorting"] = test_runner.run(test_spike_sorting)
if args.plotuncertainty:
    print "-----------------------------------------"
    print "Running testsuite: plotUncertainty"
    results["plotUncertainty"] = test_runner.run(test_plotUncertainty)
if args.features:
    print "-----------------------------------------"
    print "Running testsuite: features"
    results["features"] = test_runner.run(test_features)
if args.model:
    print "-----------------------------------------"
    print "Running testsuite: model"
    results["model"] = test_runner.run(test_model)
if args.runmodel:
    print "-----------------------------------------"
    print "Running testsuite: runModel"
    results["runModel"] = test_runner.run(test_runModel)
if args.logger:
    print "-----------------------------------------"
    print "Running testsuite: logger"
    results["logger"] = test_runner.run(test_logger)
if args.plotting:
    print "-----------------------------------------"
    print "Running testsuite: plotting"
    results["plotting"] = test_runner.run(test_plotting)
if args.usecase:
    print "-----------------------------------------"
    print "Running testsuite: usecase"
    results["usecase"] = test_runner.run(test_usecase)

total_run = 0
total_errors = 0
total_failures = 0


print "----------------------------------------------------------------------"
print "             Test summary"
print
for key in results.keys():
    errors = len(results[key].errors)
    failures = len(results[key].failures)
    run = results[key].testsRun
    print "Test: {}, run={} errors={} failures={}".format(key, run, errors, failures)

    total_run += run
    total_errors += errors
    total_failures += failures

print ""
print "Total tests run={} errors={} failures={}".format(total_run, total_errors, total_failures)


for key in results.keys():
    if not results[key].wasSuccessful():
        sys.exit(1)