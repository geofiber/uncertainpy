import numpy as np
import os
import unittest
import subprocess

from uncertainpy.plotting.plotUncertainty import PlotUncertainty
from uncertainpy.features import TestingFeatures
from uncertainpy.models import TestingModel1d

class TestPlotUncertainpy(unittest.TestCase):
    def setUp(self):
        folder = os.path.dirname(os.path.realpath(__file__))

        self.test_data_dir = os.path.join(folder, "data")
        self.data_file = "test_plot_data"
        self.output_test_dir = ".test/"


        self.plot = PlotUncertainty(data_dir=self.test_data_dir,
                                    output_dir_figures=self.output_test_dir,
                                    output_dir_gif=self.output_test_dir,
                                    verbose_level="error")



    def test_init(self):
        plot = PlotUncertainty(data_dir=self.test_data_dir,
                               output_dir_figures=self.output_test_dir,
                               output_dir_gif=self.output_test_dir,
                               verbose_level="error")

        self.assertIsInstance(plot, PlotUncertainty)


    def test_loadData(self):
        self.plot.loadData("test_save_data")

        self.assertData()


    def test_setData(self):
        self.data = PlotUncertainty(data_dir=self.test_data_dir,
                                    output_dir_figures=self.output_test_dir,
                                    output_dir_gif=self.output_test_dir,
                                    verbose_level="error")


        self.data.loadData("test_save_data")


        self.plot.setData(t=self.data.t,
                          U=self.data.U,
                          E=self.data.E,
                          Var=self.data.Var,
                          p_05=self.data.p_05,
                          p_95=self.data.p_95,
                          uncertain_parameters=self.data.uncertain_parameters,
                          sensitivity=self.data.sensitivity)

        self.assertData()


    def assertData(self):
        model = TestingModel1d()
        model.run()
        t = model.t
        U = model.U

        feature = TestingFeatures()

        self.assertTrue(np.array_equal(self.plot.t["directComparison"], t))
        self.assertTrue(np.array_equal(self.plot.t["feature1d"], t))


        self.assertTrue(self.plot.U["directComparison"].shape, (10, 21))
        self.assertTrue(self.plot.U["feature1d"].shape, (10, 21))

        self.assertTrue(np.allclose(self.plot.E["directComparison"], U, atol=0.001))
        self.assertTrue(np.allclose(self.plot.E["feature1d"], feature.feature1d(), atol=0.001))

        self.assertTrue(np.allclose(self.plot.Var["directComparison"], np.zeros(10) + 0.1, atol=0.01))
        self.assertTrue(np.allclose(self.plot.Var["feature1d"], np.zeros(10), atol=0.001))


        self.assertTrue(np.all(np.less(self.plot.p_05["directComparison"], U)))
        self.assertTrue(np.allclose(self.plot.p_05["feature1d"], feature.feature1d(), atol=0.001))

        self.assertTrue(np.all(np.greater(self.plot.p_95["directComparison"], U)))
        self.assertTrue(np.allclose(self.plot.p_95["feature1d"], feature.feature1d(), atol=0.001))

        self.assertTrue(self.plot.sensitivity["directComparison"].shape, (10, 2))
        self.assertTrue(self.plot.sensitivity["feature1d"].shape, (10, 2))

        self.assertEqual(len(self.plot.features_0d), 0)
        self.assertEqual(len(self.plot.features_1d), 2)

        self.assertEqual(len(self.plot.uncertain_parameters), 2)
        self.assertTrue(self.plot.loaded_flag)



    def test_sortFeatures(self):
        logfile = os.path.join(self.output_test_dir, "test.log")


        self.plot = PlotUncertainty(data_dir=self.test_data_dir,
                                    output_dir_figures=self.output_test_dir,
                                    output_dir_gif=self.output_test_dir,
                                    verbose_level="warning",
                                    verbose_filename=logfile)

        self.plot.loadData(self.data_file)

        features_0d, features_1d = self.plot.sortFeatures(self.plot.E)

        test_file_content = """WARNING: No support for more than 0d and 1d plotting.
WARNING: No support for more than 0d and 1d plotting."""

        self.assertTrue(test_file_content in open(logfile).read())
        self.assertEqual(features_0d, ["feature0d"])
        self.assertEqual(features_1d, ["directComparison", "feature1d"])



    def test_plotMean(self):
        self.plot.loadData(self.data_file)

        self.compare_plotType("plotMean", "mean", "directComparison")
        self.compare_plotType("plotMean", "mean", "feature1d")

        with self.assertRaises(RuntimeError):
            self.plot.plotMean(feature="feature0d")

        with self.assertRaises(RuntimeError):
            self.plot.plotMean(feature="feature2d")



    def test_plotVariance(self):
        self.plot.loadData(self.data_file)


        # self.plot.plotVariance(feature="feature1d", hardcopy=False, show=True)
        # self.plot.plotVariance(feature="directComparison", hardcopy=False, show=True)

        self.compare_plotType("plotVariance", "variance", "directComparison")
        self.compare_plotType("plotVariance", "variance", "feature1d")

        with self.assertRaises(RuntimeError):
            self.plot.plotVariance(feature="feature0d")

        with self.assertRaises(RuntimeError):
            self.plot.plotVariance(feature="feature2d")

    # def plot_assert_plotMean(self, feature):
    #     self.plot.plotMean(feature=feature)
        #
    #     folder = os.path.dirname(os.path.realpath(__file__))
    #     compare_file = os.path.join(folder, "data/plotMean_" + feature + ".png")
    #
    #     plot_file = os.path.join(self.output_test_dir, self.data_file,
    #                              feature + "_mean.png")
    #     result = subprocess.call(["diff", plot_file, compare_file])
    #
    #     self.assertEqual(result, 0)


    def compare_plotType(self, plot_type, name, feature):
        getattr(self.plot, plot_type)(feature=feature)

        folder = os.path.dirname(os.path.realpath(__file__))
        compare_file = os.path.join(folder, "data",
                                    plot_type + "_" + feature + ".png")

        plot_file = os.path.join(self.output_test_dir, self.data_file,
                                 feature + "_" + name + ".png")
        result = subprocess.call(["diff", plot_file, compare_file])

        self.assertEqual(result, 0)






if __name__ == "__main__":
    unittest.main()
