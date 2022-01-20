from falcor import *

import os 
from math import ceil,floor
from math import exp
from math import pow
import glob

import time
resultPath = 'C:/Users/admin/TestSet/'
prefix = 'res.{}.exr'


# dataPath = 'G:/MedievalNoAA/Medieval_NoAA/test4_new/MedievalDocks_Test_4/'
# mvPrefix = 'MedievalDocksMotionVector.{}.exr'

# maskPrefix = 'wrap_res/MedievalDocksWrap.{}.1.exr'

tpath = 'E:/BK_Test0_b/'
prefix = "Bunker"
def render_graph_DefaultRenderGraph():
    g = RenderGraph('DefaultRenderGraph')
    loadRenderPassLibrary('BSDFViewer.dll')
    loadRenderPassLibrary('AccumulatePass.dll')
    loadRenderPassLibrary('Antialiasing.dll')
    loadRenderPassLibrary('DepthPass.dll')
    loadRenderPassLibrary('SkyBox.dll')
    loadRenderPassLibrary('DebugPasses.dll')
    loadRenderPassLibrary('BlitPass.dll')
    loadRenderPassLibrary('CSM.dll')
    loadRenderPassLibrary('ErrorMeasurePass.dll')
    loadRenderPassLibrary('ForwardLightingPass.dll')
    loadRenderPassLibrary('GBuffer.dll')
    loadRenderPassLibrary('ImageLoader.dll')
    loadRenderPassLibrary('MegakernelPathTracer.dll')
    loadRenderPassLibrary('MinimalPathTracer.dll')
    loadRenderPassLibrary('PassLibraryTemplate.dll')
    loadRenderPassLibrary('WhittedRayTracer.dll')
    loadRenderPassLibrary('PixelInspectorPass.dll')
    loadRenderPassLibrary('SSAO.dll')
    loadRenderPassLibrary('SVGFPass.dll')
    loadRenderPassLibrary('TemporalDelayPass.dll')
    loadRenderPassLibrary('ToneMapper.dll')
    loadRenderPassLibrary('Utils.dll')
    loadRenderPassLibrary('TestWarpSpeed.dll')
    TestWarpSpeed = createPass('TestWarpSpeed', {})
    g.addPass(TestWarpSpeed, 'TestWarpSpeed')
    # ImageLoader = createPass('ImageLoader', {'filename': resultPath+prefix.format(str(11).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader, 'ImageLoader_input_1')


    # ImageLoader_ = createPass('ImageLoader', {'filename': dataPath+mvPrefix.format(str(11).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader_, 'ImageLoader_input_2')

    # ImageLoader_his = createPass('ImageLoader', {'filename': resultPath+prefix.format(str(10).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader_his, 'ImageLoader_MV1')


    # ImageLoader_occ = createPass('ImageLoader', {'filename': dataPath+mvPrefix.format(str(11).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader_occ, 'ImageLoader_MV2')

    # ImageLoader_mask = createPass('ImageLoader', {'filename': dataPath+maskPrefix.format(str(11).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader_mask, 'ImageLoader_depth1')

    # ImageLoader_d2 = createPass('ImageLoader', {'filename': dataPath+maskPrefix.format(str(11).zfill(4)), 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    # g.addPass(ImageLoader_d2, 'ImageLoader_depth2')
    
    ImageLoader0 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader1 = createPass('ImageLoader', {'filename': tpath+prefix+"MotionVector.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader2 = createPass('ImageLoader', {'filename': tpath+prefix+"WorldPosition.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader3 = createPass('ImageLoader', {'filename': tpath+prefix+"WorldNormal.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader4 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader5 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader6 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader7 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader8 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader9 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader10 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader11 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader12 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader13 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    ImageLoader14 = createPass('ImageLoader', {'filename': tpath+prefix+"PreTonemapHDRColor.0179.exr", 'mips': False, 'srgb': False, 'arrayIndex': 0, 'mipLevel': 0})
    g.addPass(ImageLoader0, 'ImageLoader0')
    g.addPass(ImageLoader1, 'ImageLoader1')
    g.addPass(ImageLoader2, 'ImageLoader2')
    g.addPass(ImageLoader3, 'ImageLoader3')
    g.addPass(ImageLoader4, 'ImageLoader4')
    g.addPass(ImageLoader5, 'ImageLoader5')
    g.addPass(ImageLoader6, 'ImageLoader6')
    g.addPass(ImageLoader7, 'ImageLoader7')
    g.addPass(ImageLoader8, 'ImageLoader8')
    g.addPass(ImageLoader9, 'ImageLoader9')
    g.addPass(ImageLoader10, 'ImageLoader10')
    g.addPass(ImageLoader11, 'ImageLoader11')
    g.addPass(ImageLoader12, 'ImageLoader12')
    g.addPass(ImageLoader13, 'ImageLoader13')
    g.addPass(ImageLoader14, 'ImageLoader14')


    

    g.addEdge('ImageLoader0.dst', 'TestWarpSpeed.gPreDemodulated')
    g.addEdge('ImageLoader1.dst', 'TestWarpSpeed.gPreMotionVectorStencil')
    g.addEdge('ImageLoader2.dst', 'TestWarpSpeed.gPreWorldPosition')
    g.addEdge('ImageLoader3.dst', 'TestWarpSpeed.gPreWorldNormal')
    g.addEdge('ImageLoader4.dst', 'TestWarpSpeed.gPrevExtraPassWarp1Frame')
    g.addEdge('ImageLoader5.dst', 'TestWarpSpeed.gPrevExtraPassWarp3Frame')
    g.addEdge('ImageLoader6.dst', 'TestWarpSpeed.gPrevExtraPassWorldPosStencil')
    g.addEdge('ImageLoader7.dst', 'TestWarpSpeed.gPrevExtraPassNormal')
    g.addEdge('ImageLoader8.dst', 'TestWarpSpeed.gForwardMotionVector')
    g.addEdge('ImageLoader9.dst', 'TestWarpSpeed.gMotionVector')
    g.addEdge('ImageLoader10.dst', 'TestWarpSpeed.gStencil')
    g.addEdge('ImageLoader11.dst', 'TestWarpSpeed.gWorldPos')
    g.addEdge('ImageLoader12.dst', 'TestWarpSpeed.gNoV')
    g.addEdge('ImageLoader13.dst', 'TestWarpSpeed.gWorldNormal')
    g.addEdge('ImageLoader14.dst', 'TestWarpSpeed.gDepthMetallicRoughness')



    g.markOutput('TestWarpSpeed.OutColor')
    return g

    
resizeSwapChain(1280, 720)

DefaultRenderGraph = render_graph_DefaultRenderGraph()
try: m.addGraph(DefaultRenderGraph)
except NameError: None


#renderFrame()
#outDir = "D:/Falcor-master"

#fc.outputDir = outDir
# fc.capture()
