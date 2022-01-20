/***************************************************************************
 # Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
 #
 # Redistribution and use in source and binary forms, with or without
 # modification, are permitted provided that the following conditions
 # are met:
 #  * Redistributions of source code must retain the above copyright
 #    notice, this list of conditions and the following disclaimer.
 #  * Redistributions in binary form must reproduce the above copyright
 #    notice, this list of conditions and the following disclaimer in the
 #    documentation and/or other materials provided with the distribution.
 #  * Neither the name of NVIDIA CORPORATION nor the names of its
 #    contributors may be used to endorse or promote products derived
 #    from this software without specific prior written permission.
 #
 # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS "AS IS" AND ANY
 # EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 # PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 # CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 # EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 # PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 # PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 # OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 # (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 # OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 **************************************************************************/
#include "TestWarpSpeed.h"

// Don't remove this. it's required for hot-reload to function properly
extern "C" __declspec(dllexport) const char* getProjDir()
{
    return PROJECT_DIR;
}

extern "C" __declspec(dllexport) void getPasses(Falcor::RenderPassLibrary& lib)
{
    lib.registerClass("TestWarpSpeed", "Render Pass Template", TestWarpSpeed::create);
}


namespace {
    const char kOutput[] = "OutColor";
    const char gPreDemodulated[] = "gPreDemodulated";
    const char gPreMotionVectorStencil[] = "gPreMotionVectorStencil";
    const char gPreWorldPosition[] = "gPreWorldPosition";
    const char gPreWorldNormal[] = "gPreWorldNormal";
    const char gPrevExtraPassWarp1Frame[] = "gPrevExtraPassWarp1Frame";
    const char gPrevExtraPassWarp3Frame[] = "gPrevExtraPassWarp3Frame";
    const char gPrevExtraPassWorldPosStencil[] = "gPrevExtraPassWorldPosStencil";
    const char gPrevExtraPassNormal[] = "gPrevExtraPassNormal";
    const char gForwardMotionVector[] = "gForwardMotionVector";
    const char gMotionVector[] = "gMotionVector";
    const char gStencil[] = "gStencil";
    const char gWorldPos[] = "gWorldPos";
    const char gNoV[] = "gNoV";
    const char gWorldNormal[] = "gWorldNormal";
    const char gDepthMetallicRoughness[] = "gDepthMetallicRoughness";
    const char kWarp[] = "RenderPasses/TestWarpSpeed/Warp.ps.slang";
}

TestWarpSpeed::TestWarpSpeed() {
    mpWarpPass = FullScreenPass::create(kWarp);
    mpFbo = Fbo::create();


    Sampler::Desc samplerDesc;
    samplerDesc.setFilterMode(Sampler::Filter::Linear, Sampler::Filter::Linear, Sampler::Filter::Linear);
    samplerDesc.setAddressingMode(Sampler::AddressMode::Clamp, Sampler::AddressMode::Clamp, Sampler::AddressMode::Clamp);
    samplerDesc.setBorderColor(Falcor::float4(0, 0, 0, 0));
    mpLinearSampler = Sampler::create(samplerDesc);
}

TestWarpSpeed::SharedPtr TestWarpSpeed::create(RenderContext* pRenderContext, const Dictionary& dict)
{
    SharedPtr pPass = SharedPtr(new TestWarpSpeed);
    return pPass;
}

Dictionary TestWarpSpeed::getScriptingDictionary()
{
    return Dictionary();
}

RenderPassReflection TestWarpSpeed::reflect(const CompileData& compileData)
{
    // Define the required resources here
    RenderPassReflection reflector;
    //reflector.addOutput("dst");
    //reflector.addInput("src");
    reflector.addInput(gPreDemodulated, "gPreDemodulated");
    reflector.addInput(gPreMotionVectorStencil, "gPreMotionVectorStencil");
    reflector.addInput(gPreWorldPosition, "gPreWorldPosition");
    reflector.addInput(gPreWorldNormal, "gPreWorldNormal");
    reflector.addInput(gPrevExtraPassWarp1Frame, "gPrevExtraPassWarp1Frame");
    reflector.addInput(gPrevExtraPassWarp3Frame, "gPrevExtraPassWarp3Frame");
    reflector.addInput(gPrevExtraPassWorldPosStencil, "gPrevExtraPassWorldPosStencil");
    reflector.addInput(gPrevExtraPassNormal, "gPrevExtraPassNormal");
    reflector.addInput(gForwardMotionVector, "gForwardMotionVector");
    reflector.addInput(gMotionVector, "gMotionVector");
    reflector.addInput(gStencil, "gStencil");
    reflector.addInput(gWorldPos, "gWorldPos");
    reflector.addInput(gNoV, "gNoV");
    reflector.addInput(gWorldNormal, "gWorldNormal");
    reflector.addInput(gDepthMetallicRoughness, "gDepthMetallicRoughness");
    reflector.addOutput(kOutput, "output color").format(ResourceFormat::RGBA32Float);

    return reflector;
}

void TestWarpSpeed::execute(RenderContext* pRenderContext, const RenderData& renderData)
{
    if (result1 == nullptr) {
        const auto& pColorOut = renderData[kOutput]->asTexture();
        result1 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        result2 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        mask0 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        mask1 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        mask2 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        mask3 = Texture::create2D(pColorOut->getWidth(), pColorOut->getHeight(), pColorOut->getFormat(), 1, 1, nullptr, Resource::BindFlags::RenderTarget | Resource::BindFlags::ShaderResource);
        
    }
    // renderData holds the requested resources
    // auto& pTexture = renderData["src"]->asTexture();
    mpFbo->attachColorTarget(renderData[kOutput]->asTexture(), 0);
    mpFbo->attachColorTarget(result1, 1);
    mpFbo->attachColorTarget(result2, 2);
    mpFbo->attachColorTarget(mask0, 3);
    mpFbo->attachColorTarget(mask1, 4);
    mpFbo->attachColorTarget(mask2, 5);
    mpFbo->attachColorTarget(mask3, 6);
    mpFbo->attachDepthStencilTarget(nullptr);

    mpWarpPass["gPreDemodulated"] = renderData[gPreDemodulated]->asTexture();
    mpWarpPass["gPreMotionVectorStencil"] = renderData[gPreMotionVectorStencil]->asTexture();
    mpWarpPass["gPreWorldPosition"] = renderData[gPreWorldPosition]->asTexture();
    mpWarpPass["gPreWorldNormal"] = renderData[gPreWorldNormal]->asTexture();
    mpWarpPass["gPrevExtraPassWarp1Frame"] = renderData[gPrevExtraPassWarp1Frame]->asTexture();
    mpWarpPass["gPrevExtraPassWarp3Frame"] = renderData[gPrevExtraPassWarp3Frame]->asTexture();
    mpWarpPass["gPrevExtraPassWorldPosStencil"] = renderData[gPrevExtraPassWorldPosStencil]->asTexture();
    mpWarpPass["gPrevExtraPassNormal"] = renderData[gPrevExtraPassNormal]->asTexture();
    mpWarpPass["gForwardMotionVector"] = renderData[gForwardMotionVector]->asTexture();
    mpWarpPass["gMotionVector"] = renderData[gMotionVector]->asTexture();

    mpWarpPass["gStencil"] = renderData[gStencil]->asTexture();
    mpWarpPass["gWorldPos"] = renderData[gWorldPos]->asTexture();
    mpWarpPass["gNoV"] = renderData[gNoV]->asTexture();
    mpWarpPass["gWorldNormal"] = renderData[gWorldNormal]->asTexture();
    mpWarpPass["gDepthMetallicRoughness"] = renderData[gDepthMetallicRoughness]->asTexture();


    mpWarpPass["gSampler"] = mpLinearSampler;

    mpWarpPass->execute(pRenderContext, mpFbo);

}

void TestWarpSpeed::renderUI(Gui::Widgets& widget)
{
}
