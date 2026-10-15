---
name: eigen
title: Eigen
area: native
tags: [cpp, linear-algebra, eigen, matrix, simd, numerics, aliasing]
detect: [dep:eigen3, dep:eigen, file:FindEigen3.cmake]
related: [cpp-modern, simd, cmake, vcpkg, googletest]
---
Eigen linear algebra: expression templates, auto and aliasing traps, alignment, decompositions, and numeric tolerance in tests.

## Verify
- `cmake --build build -j`: configure uses `find_package(Eigen3 REQUIRED NO_MODULE)` and links `Eigen3::Eigen`.
- `ctest --test-dir build --output-on-failure`: numeric tests pass with tolerances.
- `cmake -B build-dbg -DCMAKE_BUILD_TYPE=Debug && cmake --build build-dbg && ctest --test-dir build-dbg`: asserts stay on in Debug and catch size mismatches and out-of-range indices.
- `grep -rn "auto .*=.*[*+]" src | head`: find `auto` bound to an expression template.

## Test first
Compare against a known result with a relative tolerance, and check shapes.
```cpp
TEST(Solve, RecoversKnownSolution) {
    Eigen::Matrix3d A; A << 4,1,0, 1,3,1, 0,1,2;
    Eigen::Vector3d x_true(1, -2, 3);
    Eigen::Vector3d b = A * x_true;
    Eigen::Vector3d x = A.ldlt().solve(b);
    EXPECT_TRUE(x.isApprox(x_true, 1e-10));
}
```

## Do
- Link the imported target `Eigen3::Eigen` so include paths propagate; do not hard-code include dirs.
- Use fixed-size types (`Matrix3d`, `Vector4f`) for small, known sizes and `MatrixXd` for dynamic.
- Pick the decomposition for the problem: `ldlt()` for SPD, `colPivHouseholderQr()` or `completeOrthogonalDecomposition()` for least squares, `SelfAdjointEigenSolver` for symmetric eigen, `BDCSVD` for SVD.
- Check solver outcome: `Eigen::ComputationInfo` via `solver.info() == Eigen::Success`.
- Build with `-O2` or `-O3` (and `-DNDEBUG` in Release): Eigen is very slow unoptimized; add `-march=native` only for non-distributed builds.
- Use `.noalias()` on products into a different destination: `C.noalias() = A * B;`.
- Use `Eigen::Map<Matrix>` over existing buffers to avoid copies, and `.eval()` when a temporary is needed.
- Use `Eigen::SparseMatrix` with `setFromTriplets` for sparse systems, and a sparse solver (`SimplicialLDLT`, `SparseLU`).

## Avoid
- `auto C = A * B;` or `auto x = a + b;`: stores an expression referencing temporaries, so it dangles. Write the concrete type or `.eval()`.
- Aliasing in assignments like `A = A.transpose();` or `A = A * B;` (dynamic): wrong results. Use `A.transposeInPlace()` or `.eval()`.
- Fixed-size vectorizable members in a class allocated with `new` before C++17: alignment crashes. Use C++17 or `EIGEN_MAKE_ALIGNED_OPERATOR_NEW`.
- `==` on floating matrices: use `isApprox` or a norm of the difference.
- Inverting a matrix to solve (`A.inverse() * b`): slower and less accurate. Use `solve`.
- Mixing `Matrix<float>` and `Matrix<double>` implicitly: compile error. Use `.cast<double>()`.
- Row-major vs column-major confusion with raw pointers: Eigen is column-major by default; declare `RowMajor` when mapping row-major data.

## Review
- [ ] No `auto` bound to Eigen expressions.
- [ ] Solver success is checked, and conditioning is considered.
- [ ] Release builds are optimized; Debug tests run with asserts on.
- [ ] Mapped buffers have the right storage order and lifetime.
- [ ] Float comparisons use tolerances.
