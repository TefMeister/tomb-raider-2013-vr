# 2026-10-01 /pd: the .tiger shaders do not read StereoOffset

`../../tools/tiger_cdrm_scan.py` walked all four `bigfile.*.tiger` parts: 171,698 CDRM containers parsed with no error,
25,047 compiled shaders (DXBC) found after inflating, 21,008 containers mentioning `SceneBuffer`, and **0** mentioning
`StereoOffset` (a shader's reflection carries every declared variable name, so none declares it).
`material-SceneBuffer-layout.txt`: the material shaders' `SceneBuffer` (1,200 bytes) from a 40-container sample,
listed with `dxbc-reflect.py`. Interface metadata only; no shader is kept here.
