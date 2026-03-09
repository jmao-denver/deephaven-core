cmake -B build -S . `
-DCMAKE_TOOLCHAIN_FILE="$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" `
-DCMAKE_INSTALL_PREFIX="$env:FLIGHT_SQL_ODBC_INSTALL_DIR" `
-DCMAKE_PREFIX_PATH="c:/git/arrow/cpp/vcpkg_installed/x64-windows" `
-DArrow_DIR=C:/flight_sql_odbc_install `
-DX_VCPKG_APPLOCAL_DEPS_INSTALL=ON
