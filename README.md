# Rust for Haiku / RENKU

Haiku/RENKU용 비공식 Rust 패키지와 ARM64 포팅·빌드 스크립트입니다.
현재 이 프로젝트가 직접 배포하는 패키지는 ARM64용 `rust_bin` 1.90.0-3이며,
`rustc`, Cargo, `rustdoc`, 표준 라이브러리를 포함합니다.

## 비공식 배포 및 문의 안내

**이 패키지는 Rust 프로젝트의 공식 배포판이 아닙니다.** Rust 프로젝트나
Rust Foundation이 제작·승인·지원하는 패키지가 아닙니다.
Rust Foundation에 문의하지 마세요.

**Unofficial distribution:** This package is not an official Rust release and is
not endorsed or supported by the Rust Project or the Rust Foundation.
Do not contact the Rust Foundation.

## 라이선스

Rust 자체는 사용자가 선택하는 **MIT 또는 Apache License 2.0** 조건으로
배포됩니다. 이 패키지의 Rust 구성 요소도 해당 라이선스를 따르며,
원저작자의 권리와 고지를 유지합니다. 원본 라이선스와 저작권 안내는
[LICENSE-MIT](LICENSE-MIT), [LICENSE-APACHE](LICENSE-APACHE),
[COPYRIGHT](COPYRIGHT)에 포함되어 있습니다.

이 저장소에서 새로 작성한 포팅·패키징 스크립트 역시 별도 표시가 없으면
`MIT OR Apache-2.0`으로 제공합니다. 원본 파일의 저작권 표시는 그대로 유지합니다.
LLVM, Cargo의 의존 라이브러리, OpenSSL, zlib 등 제3자 구성 요소에는 각각의
라이선스와 고지가 적용됩니다. Rust의 라이선스가 모든 의존성의 라이선스를
대체하는 것은 아닙니다. 구성 요소별 정보는
[Rust 1.90.0 저작권 안내](https://github.com/rust-lang/rust/blob/1.90.0/COPYRIGHT)와
[라이선스 메타데이터](https://github.com/rust-lang/rust/blob/1.90.0/license-metadata.json)를 참고하세요.

## 아키텍처별 설치 경로

아래 상태는 2026-10-07 기준입니다. Haiku 아키텍처 이름과 Rust target 이름은
다르므로 혼동하지 마세요. 이 저장소가 다른 아키텍처용 `rust_bin` HPKG도 배포한다는
뜻은 아닙니다.

| Haiku 아키텍처 | Rust target | 패키지 및 제공처 | 확인 상태 |
| --- | --- | --- | --- |
| `arm64` | `aarch64-unknown-haiku` | 이 프로젝트의 `rust_bin`, pkgman.rainygirl.com | 설치·네이티브 빌드·실행 검증 완료, 실험적 포트 |
| `x86_64` | `x86_64-unknown-haiku` | HaikuPorts의 `rust_bin` | upstream 레시피 확인; 이 프로젝트에서 실행 검증하지 않음 |
| `x86_gcc2` + 보조 `x86` ABI | `i686-unknown-haiku` | HaikuPorts의 `rust_bin_x86` | 보조 아키텍처 레시피 확인; 이 프로젝트에서 실행 검증하지 않음 |
| 순수 `x86` | `i686-unknown-haiku` | HaikuPorts 저장소에서 제공할 경우 `rust_bin` | upstream에서 `?x86`; 설치 가능 여부 미검증 |
| ARM 32비트, RISC-V, PowerPC 등 | 해당 target별로 다름 | 이 프로젝트의 설치 패키지 없음 | 미지원 |

### 공통 준비: 시간과 CA 인증서

시스템 날짜·시간을 먼저 맞추세요. HTTPS 검증에 기본 CA 인증서가 필요합니다.
기존 HTTPS 패키지 다운로드가 정상이라면 다음으로 설치할 수 있습니다.

```sh
pkgman install ca_root_certificates
```

새 ARM64 이미지에 CA가 없어 위 명령도 실패한다면, 신뢰하는 다른 컴퓨터에서
다음 파일을 **HTTPS 인증서 검증을 유지한 상태로** 다운로드한 뒤 USB나 이미
검증된 SSH 연결로 Haiku에 옮기세요.

```sh
curl -fLO https://pkgman.rainygirl.com/arm64-webpositive/packages/ca_root_certificates-2025_12_02-1-any.hpkg
```

이 파일을 `/boot/home`에 옮긴 경우 Haiku에서:

```sh
sha256sum /boot/home/ca_root_certificates-2025_12_02-1-any.hpkg
pkgman install /boot/home/ca_root_certificates-2025_12_02-1-any.hpkg
```

예상 SHA-256:

```text
af715a80786abc133d1313f94da4a1a1ffde7242a722c2c29f3eb22241a69efc
```

체크섬이 다르면 설치하지 마세요. `curl -k`나 인증서 검증 비활성화로 우회하지
않습니다. 이 파일은 초기 설치용 고정 버전이며 이후 인증서 업데이트도 유지하세요.

### ARM64 (`arm64`)

Haiku ARM64/RENKU ARM64에서 실행합니다. 다음 저장소 중 `arm64-system`은
시스템·개발 도구, `arm64-webpositive`는 OpenSSL·CA 등 의존성을 제공합니다.
특히 시스템 저장소를 추가하면 이후 패키지 작업에서 RENKU 시스템 패키지도
후보가 되므로, 다른 시스템 이미지는 호환성을 확인한 뒤 사용하세요.
검증 환경은 RENKU ARM64 `hrev60071+15`, GCC 13.3.0입니다.

```sh
pkgman add-repo https://pkgman.rainygirl.com/arm64
pkgman add-repo https://pkgman.rainygirl.com/arm64-system
pkgman add-repo https://pkgman.rainygirl.com/arm64-webpositive
pkgman refresh
pkgman install rust_bin
```

이미 같은 저장소가 HTTP로 등록되어 있으면 HTTPS 주소로 덮어쓰는 질문에
동의하세요. 설치 변경 목록을 확인한 뒤 진행하세요. GCC, binutils, 개발 헤더,
OpenSSL, CA 인증서 등 필요한 패키지는 의존성으로 지정되어 있습니다.

정식 패키지명은 **`rust_bin`**입니다. 이전 `rust-1.90.0-2` 설치본은 자동으로
대체되며, `rust`는 기존 의존성을 위한 호환성 제공 이름으로만 남습니다.
초기 `rust_bin-1.90.0-1` 설치본은 같은 이름의 새 리비전으로 업데이트됩니다.

```sh
rustc -vV
cargo -V
rustdoc -V
```

`rustc -vV`의 `host`가 `aarch64-unknown-haiku`인지 확인하세요.
이 ARM64 패키지에 rustup, rustfmt, Clippy 또는 다른 target의 표준 라이브러리는
포함되어 있지 않습니다. `rustup target add`로 이 포트를 설치하는 방법도
제공하지 않습니다.

현재 HPKG: [rust_bin-1.90.0-3-arm64.hpkg](https://pkgman.rainygirl.com/arm64/packages/rust_bin-1.90.0-3-arm64.hpkg)

```text
SHA-256: ae809424af17b6358a4fc230c8f8a1f4d288b6a82dd011031cc850f7a75c4fa3
```

### x86_64 (64비트 Intel/AMD)

기본 HaikuPorts 저장소를 사용하는 설치 방법입니다. ARM64용 RENKU 시스템
저장소를 x86_64에 추가하지 마세요.

```sh
pkgman refresh
pkgman install rust_bin
rustc -vV
cargo -V
```

예상 target은 `x86_64-unknown-haiku`입니다. 패키지명은 ARM64와 같은
`rust_bin`이지만, x86_64 패키지는 HaikuPorts에서 제공합니다.
버전과 설치 가능 여부는 사용 중인 HaikuPorts 저장소에 따릅니다.

### x86_gcc2 / 32비트 Haiku의 보조 x86 ABI

GCC2 ABI용 Rust는 제공하지 않습니다. 32비트 하이브리드 시스템에서는 현대
GCC 기반 보조 `x86` 아키텍처 패키지를 설치합니다.

```sh
pkgman refresh
pkgman install rust_bin_x86
setarch x86
rustc -vV
cargo -V
```

`setarch x86`으로 보조 아키텍처 셸에 진입한 뒤 Rust를 사용합니다.
예상 target은 `i686-unknown-haiku`입니다. 작업이 끝나면 `exit`로 나옵니다.
링커를 사용하는 빌드에는 해당 ABI의 GCC·binutils·개발 헤더도 필요합니다.

### 순수 x86 및 그 외 아키텍처

순수 현대 GCC 기반 `x86` 시스템은 `pkgman search rust`로 저장소의 실제
제공 여부를 먼저 확인하세요. 해당 아키텍처용 `rust_bin`이 검색될 때만
`pkgman install rust_bin`을 사용합니다. 하이브리드용 안내를 그대로 적용하거나
ARM64 HPKG를 설치하지 마세요. 이 프로젝트는 순수 x86 설치를 검증하지 않았습니다.

ARM 32비트·RISC-V·PowerPC 등은 이 프로젝트에서 배포하는 설치 패키지가 없습니다.

x86 계열 안내의 근거:
[HaikuPorts rust_bin 레시피](https://github.com/haikuports/haikuports/blob/f2acc6a8e632856af2d6ba9e8bd41e5b8701e3d7/dev-lang/rust_bin/rust_bin-1.94.1.recipe).
레시피 지원 표시가 모든 Haiku 릴리스 저장소의 바이너리 제공을 보장하지는 않습니다.

## ARM64 검증 내역

QEMU의 설치된 RENKU ARM64 게스트에서 다음을 검증했습니다.

- HTTPS 저장소를 통한 `pkgman install rust_bin`과 기존 `rust`의 자동 대체
- 네이티브 Rust 컴파일·실행, 스레드·atomic·panic unwinding
- 파일 I/O, TCP, 자식 프로세스 실행
- procedural macro 컴파일 및 동적 로딩
- `cargo run`, 단위 테스트, rustdoc 문서 테스트
- 기본 CA를 이용한 crates.io HTTPS 검색·다운로드와 내려받은 크레이트의 빌드

저장소의 테스트를 실행하려면 설치된 도구체인이 PATH에 있는 상태에서:

```sh
bash test-native.sh
```

## 빌드 스크립트

이 저장소에는 Rust 전체 소스나 바이너리를 넣지 않고 ARM64 target 정의,
빌드 설정, 패키지 메타데이터와 테스트를 포함합니다.
빌드 스크립트는 완성된 일괄 설치기가 아니라 검증에 사용한 빌드 환경용입니다.
Linux ARM64 빌드 호스트, Haiku ARM64 크로스 GCC 13.3.0, 실제 게스트에서 내보낸
sysroot, Rust 1.90.0 원본 소스 및 OpenSSL 소스를 먼저 준비해야 합니다.
Linux 시스템 헤더를 Haiku sysroot에 대신 넣지 마세요.

주요 고정 경로는 `/work/rustc-1.90.0-src`, `/exchange/rust-port`(이 저장소),
`/opt/haiku/cross-tools-arm64`이며 필요하면 설정과 스크립트를 함께 조정하세요.
Rust 소스는 upstream의 SHA-256 파일로 검증한 뒤 사용합니다.
`build-openssl.sh`는 `/work/openssl-3.5.4`와 해당 소스 압축 파일·체크섬을
이미 준비했다고 가정합니다.

```sh
bash build-openssl.sh
bash build-zlib.sh
bash build.sh
```

`stage-package.py --help`로 패키지 조립 인수를 확인하세요. 이 스크립트는
Haiku용 실행 파일과 표준 라이브러리를 선택하고 Linux용 바이너리의 혼입을
검사합니다. 전송용 tar는 BFS의 hardlink 제한 때문에 `--hard-dereference`를
사용하며, HPKG 생성은 Haiku의 `package create`로 수행합니다.
