import numpy as np

solution = np.array([0.0,
                  10.0,
                  46.71216431663565,
                  78.00990165025024,
                  123.1022296947644,
                  178.36200402451087,
                  226.2535557452701,
                  279.47277814492026,
                  322.5596836489306,
                  380.35465583865783,
                  430.01302764182446,
                  465.51703339349143,
                  508.0407829196081,
                  558.3722178620411,
                  638.6451197769284,
                  692.4262545843217,
                  739.862904910141,
                  793.6868577161139,
                  830.3999102662548,
                  883.268153466554,
                  909.2356594788534,
                  958.7064300074014,
                  998.375133772232,
                  1044.2865763217396,
                  1100.0284905299168,
                  1144.111334989716,
                  1182.8878881027836,
                  1221.706733772139,
                  1265.555641115047,
                  1332.7371251782072,
                  1384.0920325928969,
                  1432.3575309850808,
                  1479.8002509265305,
                  1526.8973851959422,
                  1562.9118499691072,
                  1614.565716794311,
                  1653.5171204297944,
                  1696.4285683624787,
                  1738.5082678851522,
                  1775.2706318977994,
                  1814.2190375314997,
                  0.0,
                  10.712164316635647,
                  15.297737333614592,
                  21.092328044514165,
                  29.25977432974647,
                  19.89155172075923,
                  25.219222399650167,
                  21.08690550401036,
                  29.79497218972723,
                  29.658371803166634,
                  17.50400575166694,
                  22.523749526116664,
                  26.331434942433,
                  52.27290191488729,
                  29.78113480739334,
                  25.436650325819326,
                  27.82395280597287,
                  26.713052550140944,
                  32.86824320029926,
                  17.96750601229936,
                  23.47077052854792,
                  27.668703764830504,
                  17.911442549507562,
                  29.741914208177196,
                  28.08284445979922,
                  24.776553113067735,
                  18.818845669355305,
                  21.84890734290797,
                  39.181484063160326,
                  29.354907414689773,
                  20.26549839218379,
                  25.442719941449777,
                  29.097134269411644,
                  28.014464773164917,
                  27.653866825203668,
                  18.951403635483416,
                  24.911447932684354,
                  22.079699522673447,
                  18.762364012647105,
                  20.94840563370039,
                  12.78096246850032,
                  2447.0,
                  9121.0,
                  9595.0,
                  3068.0,
                  4827.0,
                  8611.0,
                  2850.0,
                  5037.0,
                  422.0,
                  390.0,
                  6345.0,
                  4935.0,
                  9588.0,
                  2675.0,
                  1409.0,
                  8942.0,
                  8706.0,
                  6018.0,
                  3709.0,
                  1364.0,
                  6225.0,
                  2999.0,
                  4411.0,
                  892.0,
                  333.0,
                  4933.0,
                  6222.0,
                  7060.0,
                  189.0,
                  854.0,
                  4948.0,
                  8485.0,
                  8078.0,
                  1947.0,
                  8717.0,
                  1658.0,
                  7664.0,
                  4397.0,
                  555.0,
                  13.0,
                  735.0])

# Solution.txt erstellen
with open("Solution.txt", "w") as output:
    output.write("[")
    for ele in solution:
        output.write(f"{ele}, ")
    output.write("]")
