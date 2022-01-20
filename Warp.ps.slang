
Texture2D<float4> gPreDemodulated;
Texture2D<float4> gPreMotionVectorStencil; // 
Texture2D<float4> gPreWorldPosition;
Texture2D<float4> gPreWorldNormal;

Texture2D<float4> gPrevExtraPassWarp1Frame; 
Texture2D<float4> gPrevExtraPassWarp3Frame; 
Texture2D<float4> gPrevExtraPassWorldPosStencil; 
Texture2D<float3> gPrevExtraPassNormal; 

Texture2D<float4>  gForwardMotionVector;  
Texture2D<float4>  gMotionVector;       // TODO: depth???
Texture2D<float4>  gStencil;            // TODO: 
Texture2D<float4>  gWorldPos;           // TODO: 
Texture2D<float4>  gNoV;                // TODO:


Texture2D<float4>  gWorldNormal;                // TODO: 
Texture2D<float4>  gDepthMetallicRoughness;                // TODO: 



SamplerState gSampler;

struct PSOut
{
    float4 Color0             : SV_TARGET0;
    float4 Color1             : SV_TARGET1;
    float4 Color2             : SV_TARGET2;
    float4 WarpOcc             : SV_TARGET3;
    float4 WorldPosStencil     : SV_TARGET4;
    float4 Normal             : SV_TARGET5;
    float4 Feature             : SV_TARGET6;
};

float3 Tonemap(float3 beforeToneValue){
    return log(1.0 + beforeToneValue);
}
float MakeMask(float3 currWorldPos, float3 prevWorldPos, float currStencil, float prevStencil, float3 currNormal, float3 prevWorldNormal, float bias)
{
    bool dynamicHole = abs(currStencil - prevStencil) > 1e-4;
    bool selfOcclusion = dot(currNormal, prevWorldNormal) < 0.98;
    bool staticHole = length(currWorldPos - prevWorldPos) > bias;

    
    return dynamicHole || selfOcclusion || staticHole ? 0.0 : 1.0;
}

PSOut main(float2 texC : TEXCOORD) : SV_TARGET0
{
    PSOut pou;


    const int2 texDim = int2(1280, 720);

    //// UV
    //float2 UV = pixelPos2UV(PixelPos, texDim);
    //FGBufferData GBuffer = GetGBufferDataFromSceneTextures(UV);

    float3 featureValue = gDepthMetallicRoughness.Sample(gSampler, texC).xyz;


    float2 originMv = gMotionVector.Sample(gSampler, texC).xy;
    

    float2 prevUV = texC - float2(originMv.x, -1 * originMv.y) / texDim;
    float3 preOriginMvStencil = gPreMotionVectorStencil.Sample(gSampler, prevUV).xyz;

    float2 prevPrevUV = prevUV - float2(preOriginMvStencil.x, -1 * preOriginMvStencil.y) / texDim;


    // occ mv
    float2 forwardMvValue = gForwardMotionVector.Sample(gSampler, prevUV).xy;
    float2 occUv = prevUV - float2(forwardMvValue.x, -forwardMvValue.y) / texDim;
    float3 warpOccValue = gPreDemodulated.Sample(gSampler, occUv).xyz;


    float3 warp1Value = gPreDemodulated.Sample(gSampler, prevUV).xyz;
    float4 warp3Value = gPrevExtraPassWarp1Frame.Sample(gSampler, prevPrevUV);
    float4 warp5Value = gPrevExtraPassWarp3Frame.Sample(gSampler, prevPrevUV);


    float3 currWorldPos = gWorldPos.Sample(gSampler, texC).xzy;
    float currStencil = gStencil.Sample(gSampler, texC).x;
    float currNoV = gNoV.Sample(gSampler, texC).x;


    
    float3 currNormal = gWorldNormal.Sample(gSampler, texC).xyz;
    float3 currMetallicDepthRoughness = gDepthMetallicRoughness.Sample(gSampler, texC).xyz;

    float currMetallic = currMetallicDepthRoughness.x;
    float currRoughness = currMetallicDepthRoughness.y;
    float currDepth = currMetallicDepthRoughness.z; // TODO:     DEPTH

    float bias = lerp(7.5, 45, abs( currNoV ) ) + currDepth * 50; 


    float3 prevWorldPos = gPreWorldPosition.Sample(gSampler, prevUV).xyz;
    float3 prevWorldNormal = normalize(gPreWorldNormal.Sample(gSampler, prevUV).xyz);
    float prevStencil = preOriginMvStencil.z;

    float4 prevExtraWorldPosStencil = gPrevExtraPassWorldPosStencil.Sample(gSampler, prevPrevUV);
    float3 prevExtraWorldNormal = normalize(gPrevExtraPassNormal.Sample(gSampler, prevPrevUV).xyz);


    // float3 warp1ValueDetoned = DeTonemap(warp1Mask.xyz);
    // float3 warp3ValueDetoned = DeTonemap(warp3Mask.xyz);

    // TODO: 历史的mask  warp？？？
    float mask1 = MakeMask(currWorldPos, prevWorldPos, currStencil, prevStencil, currNormal, prevWorldNormal, bias);
    float mask3 = warp3Value.w * mask1 * MakeMask(currNormal, prevExtraWorldPosStencil.xyz, currStencil, prevExtraWorldPosStencil.w, currNormal, prevExtraWorldNormal, bias);
    float mask5 = warp5Value.w * mask3;
    //float mask1 = bias * currStencil * prevStencil * dot(currWorldPos, prevWorldPos) * dot(currNormal, prevWorldNormal);
    //float mask3 = warp3Value.w * mask1 * bias * currStencil * prevExtraWorldPosStencil.w * dot(currWorldPos, prevExtraWorldPosStencil.xyz) * dot(currNormal, prevExtraWorldNormal);

    //float mask5 = warp5Value.w * mask3;
    //float mask1 = 0;
    //float mask3 = 0;
    //float mask5 = 0;

    pou.WarpOcc = float4(Tonemap(warpOccValue), 1.0);
    pou.Color0 = float4(Tonemap(warp1Value), mask1);
    pou.Color1 = float4(warp3Value.xyz, mask3); // 不detone了
    pou.Color2 = float4(warp5Value.xyz, mask5); // 不detone了
    pou.WorldPosStencil = float4(currWorldPos, currStencil);
    pou.Normal = float4(currNormal, 1.0);
    pou.Feature = float4(featureValue, 1.0);



    return pou;
}
