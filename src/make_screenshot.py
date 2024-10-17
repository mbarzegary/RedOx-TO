import argparse

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

def make_screenshot(input_dir, out_filename):
    gammafpvd = PVDReader(registrationName='gammaf.pvd', FileName=f'{input_dir}/gammaf.pvd')
    gammafpvd.PointArrays = ['gamma']

    renderView1 = GetActiveViewOrCreate('RenderView')

    gammafpvdDisplay = Show(gammafpvd, renderView1, 'UnstructuredGridRepresentation')

    gammaLUT = GetColorTransferFunction('gamma')

    gammaPWF = GetOpacityTransferFunction('gamma')

    gammafpvdDisplay.Representation = 'Surface'
    gammafpvdDisplay.ColorArrayName = ['POINTS', 'gamma']
    gammafpvdDisplay.LookupTable = gammaLUT
    gammafpvdDisplay.SelectTCoordArray = 'None'
    gammafpvdDisplay.SelectNormalArray = 'None'
    gammafpvdDisplay.SelectTangentArray = 'None'
    gammafpvdDisplay.OSPRayScaleArray = 'gamma'
    gammafpvdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    gammafpvdDisplay.SelectOrientationVectors = 'None'
    gammafpvdDisplay.ScaleFactor = 0.30000000000000004
    gammafpvdDisplay.SelectScaleArray = 'gamma'
    gammafpvdDisplay.GlyphType = 'Arrow'
    gammafpvdDisplay.GlyphTableIndexArray = 'gamma'
    gammafpvdDisplay.GaussianRadius = 0.015
    gammafpvdDisplay.SetScaleArray = ['POINTS', 'gamma']
    gammafpvdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    gammafpvdDisplay.OpacityArray = ['POINTS', 'gamma']
    gammafpvdDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    gammafpvdDisplay.DataAxesGrid = 'GridAxesRepresentation'
    gammafpvdDisplay.PolarAxes = 'PolarAxesRepresentation'
    gammafpvdDisplay.ScalarOpacityFunction = gammaPWF
    gammafpvdDisplay.ScalarOpacityUnitDistance = 0.09148345407427515
    gammafpvdDisplay.OpacityArrayName = ['POINTS', 'gamma']
    # gammafpvdDisplay.SelectInputVectors = [None, '']
    # gammafpvdDisplay.WriteLog = ''

    gammafpvdDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.9961367817146366, 1.0, 0.5, 0.0]

    gammafpvdDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.9961367817146366, 1.0, 0.5, 0.0]

    renderView1.ResetCamera(False)

    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [1.5, 0.4, 10000.0]
    renderView1.CameraFocalPoint = [1.5, 0.4, 0.0]

    materialLibrary1 = GetMaterialLibrary()

    gammafpvdDisplay.SetScalarBarVisibility(renderView1, True)

    renderView1.Update()

    # gammaTF2D = GetTransferFunction2D('gamma')

    LoadPalette(paletteName='WhiteBackground')

    renderView1.OrientationAxesVisibility = 0

    gammafpvdDisplay.SetScalarBarVisibility(renderView1, False)

    gammaLUT.ApplyPreset('Rainbow Desaturated', True)

    clip1 = Clip(registrationName='Clip1', Input=gammafpvd)
    clip1.ClipType = 'Plane'
    clip1.HyperTreeGridClipper = 'Plane'
    clip1.Scalars = ['POINTS', 'gamma']
    clip1.Value = 0.4980683908573183

    # clip1.HyperTreeGridClipper.Origin = [1.5, 0.4, 0.0]

    clip1.ClipType.Origin = [1.5, 0.5, 0.0]
    clip1.ClipType.Normal = [0.0, 1.0, 0.0]

    clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

    clip1Display.Representation = 'Surface'
    clip1Display.ColorArrayName = ['POINTS', 'gamma']
    clip1Display.LookupTable = gammaLUT
    clip1Display.SelectTCoordArray = 'None'
    clip1Display.SelectNormalArray = 'None'
    clip1Display.SelectTangentArray = 'None'
    clip1Display.OSPRayScaleArray = 'gamma'
    clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    clip1Display.SelectOrientationVectors = 'None'
    clip1Display.ScaleFactor = 0.15000000000000002
    clip1Display.SelectScaleArray = 'gamma'
    clip1Display.GlyphType = 'Arrow'
    clip1Display.GlyphTableIndexArray = 'gamma'
    clip1Display.GaussianRadius = 0.0075
    clip1Display.SetScaleArray = ['POINTS', 'gamma']
    clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
    clip1Display.OpacityArray = ['POINTS', 'gamma']
    clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
    clip1Display.DataAxesGrid = 'GridAxesRepresentation'
    clip1Display.PolarAxes = 'PolarAxesRepresentation'
    clip1Display.ScalarOpacityFunction = gammaPWF
    clip1Display.ScalarOpacityUnitDistance = 0.06305707654622791
    clip1Display.OpacityArrayName = ['POINTS', 'gamma']
    # clip1Display.SelectInputVectors = [None, '']
    # clip1Display.WriteLog = ''

    clip1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.9960439808156171, 1.0, 0.5, 0.0]

    clip1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.9960439808156171, 1.0, 0.5, 0.0]

    Hide(gammafpvd, renderView1)

    clip1Display.SetScalarBarVisibility(renderView1, True)

    renderView1.Update()

    # HideInteractiveWidgets(proxy=clip1.ClipType)

    clip1Display.SetScalarBarVisibility(renderView1, False)

    layout1 = GetLayout()

    layout1.PreviewMode = [1600, 300]

    layout1.SetSize(1600, 300)

    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [1.5, 0.25, 10000.0]
    renderView1.CameraFocalPoint = [1.5, 0.25, 0.0]
    renderView1.CameraParallelScale = 0.3

    SaveScreenshot(out_filename, layout1, ImageResolution=[1600, 300], CompressionLevel='2')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input_dir", type=str, default="./results")
    parser.add_argument("--out_name", type=str, default="./out.png")

    args, _ = parser.parse_known_args()
    input_dir = args.input_dir
    out_filename = args.out_name
    make_screenshot(input_dir, out_filename)
