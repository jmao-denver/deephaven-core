cmake -B build -S . `
-DCMAKE_INSTALL_PREFIX="$env:FLIGHT_SQL_ODBC_INSTALL_DIR" `
-DCMAKE_PREFIX_PATH="c:/git/arrow/cpp/vcpkg_installed/x64-windows" `
-DArrow_DIR=C:/flight_sql_odbc_install `
-DX_VCPKG_APPLOCAL_DEPS_INSTALL=ON `
-DCMAKE_TOOLCHAIN_FILE="C:/Program Files/Microsoft Visual Studio/2022/Community/VC/vcpkg/scripts/buildsystems/vcpkg.cmake"
