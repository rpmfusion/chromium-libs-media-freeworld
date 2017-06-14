# gn is the new new new buildtool. *sigh*
%global use_gn 1

# Leave this alone, please.
%global target out/Release

# Debuginfo packages aren't very useful here. If you need to debug
# you should do a proper debug build (not implemented in this spec yet)
%global debug_package %{nil}

# %%{nil} for Stable; -beta for Beta; -dev for Devel
# dash in -beta and -dev is intentional !
%global chromium_channel %{nil}
%global chromium_browser_channel chromium-browser%{chromium_channel}
%global chromium_path %{_libdir}/chromium-browser%{chromium_channel}
%global crd_path %{_libdir}/chrome-remote-desktop
%global tests 0

# Chromium Package name
%global cname chromium%{chromium_channel}

# We don't want any libs in these directories to generate Provides
# Requires is trickier.

%global __provides_exclude_from %{chromium_path}/.*\\.so|%{chromium_path}/lib/.*\\.so
%global privlibs libaccessibility|libaura_extra|libaura|libbase_i18n|libbase|libbindings|libblink_common|libblink_core|libblink_modules|libblink_platform|libblink_web|libbluetooth|libboringssl|libbrowser_ui_views|libcaptive_portal|libcapture|libcapture_base|libcapture_lib|libcc_animation|libcc_blink|libcc_ipc|libcc_paint|libcc_proto|libcc|libcc_surfaces|libchromium_sqlite3|libclearkeycdm|libcloud_policy_proto_generated_compile|libcommon|libcompositor|libcontent|libcpp|libcrcrypto|libdbus|libdevice_base|libdevice_battery|libdevice_event_log|libdevice_gamepad|libdevices|libdevice_vibration|libdevice_vr|libdiscardable_memory_client|libdiscardable_memory_common|libdiscardable_memory_service|libdisplay_compositor|libdisplay|libdisplay_types|libdisplay_util|libdomain_reliability|libEGL|libevents_base|libevents_devices_x11|libevents_ipc|libevents_ozone_layout|libevents|libevents_x|libfingerprint|libffmpeg|libfont_service_library|libgcm|libgeneric_sensor|libgeolocation|libgeometry|libgesture_detection|libgfx_ipc_color|libgfx_ipc_geometry|libgfx_ipc_skia|libgfx_ipc|libgfx|libgfx_x11|libgin|libgles2_c_lib|libgles2_implementation|libgles2_utils|libGLESv2|libgl_in_process_context|libgl_init|libgl_wrapper|libgpu|libgtk2ui|libicui18n|libicuuc|libipc|libjs|libkeyboard|libkeyboard_with_content|libkeycodes_x11|libkeyed_service_content|libkeyed_service_core|libmedia_blink|libmedia_gpu|libmedia|libmessage_center|libmidi|libmojo_common_lib|libmojo_ime_lib|libmojo_public_system_cpp|libmojo_public_system|libmojo_system_impl|libnative_theme|libnet|libnet_with_v8|libonc|libplatform|libpolicy_component|libpolicy_proto|libpower_monitor|libpower_save_blocker|libppapi_host|libppapi_proxy|libppapi_shared|libprefs|libprinting|libprotobuf_lite|libproxy_config|librange|libsandbox_services|libseccomp_bpf|libsensors|libsessions|libshared_memory_support|libshell_dialogs|libskia|libsnapshot|libsql|libstartup_tracing|libstorage_browser|libstorage_common|libstub_window|libsuid_sandbox_client|libsurface|libtest_ime_driver_library|libtime_zone_monitor|libtracing_library|libtracing|libui_base_ime|libui_base|libui_base_x|libui_data_pack|libui_library|libui_touch_selection|libui_views_mus_lib|liburl_ipc|liburl_matcher|liburl|libuser_manager|libuser_prefs|libv8_libbase|libv8_libplatform|libv8|libviews|libwebdata_common|libweb_dialogs|libwebview|libwidevinecdmadapter|libwidevinecdm|libwm|libwtf|libx11_events_platform|libx11_window
%global __requires_exclude ^(%{privlibs})\\.so

# Try to not use the Xvfb as it is slow..
%global tests_force_display 0

# AddressSanitizer mode
# https://www.chromium.org/developers/testing/addresssanitizer
%global asan 0

# We don't need this to compile only the codecs
%global killnacl 1

%if 0%{?killnacl}
 %global nacl 0
 %global nonacl 1
%else
# TODO: Try arm (nacl disabled)
%if 0%{?fedora}
 %ifarch i686
 %global nacl 0
 %global nonacl 1
 %else
 %global nacl 1
 %global nonacl 0
 %endif
%endif
%endif

%if 0
# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
BuildRequires:	libicu-devel >= 5.4
%global bundleicu 0
%else
%global bundleicu 1
%endif

%global bundlere2 1

%if 0%{?rhel} == 7
%global bundleopus 1
%global bundlelibusbx 1
%global bundleharfbuzz 1
%else
%global bundleharfbuzz 0
%global bundleopus 1
%global bundlelibusbx 0
%endif

### Google API keys (see http://www.chromium.org/developers/how-tos/api-keys)
### Note: These are for Fedora use ONLY.
### For your own distribution, please get your own set of keys.
### http://lists.debian.org/debian-legal/2013/11/msg00006.html
%global api_key AIzaSyDUIXvzVrt5OkVsgXhQ6NFfvWlA44by-aw
%global default_client_id 449907151817.apps.googleusercontent.com
%global default_client_secret miEreAep8nuvTdvLums6qyLK
%global chromoting_client_id 449907151817-8vnlfih032ni8c4jjps9int9t86k546t.apps.googleusercontent.com

%global majorversion 58

Name:		%{cname}-libs-media-freeworld
Version:	%{majorversion}.0.3029.110
Release:	2%{?dist}
Summary:        Chromium media libraries built with all possible codecs
Url:		http://www.chromium.org/Home
License:	BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)

### Chromium Fedora Patches ###
Patch0:		chromium-56.0.2924.87-gcc5.patch
Patch1:		chromium-45.0.2454.101-linux-path-max.patch
Patch2:		chromium-55.0.2883.75-addrfix.patch
Patch4:		chromium-46.0.2490.71-notest.patch
# In file included from ../linux/directory.c:21:
# In file included from ../../../../native_client/src/nonsfi/linux/abi_conversion.h:20:
# ../../../../native_client/src/nonsfi/linux/linux_syscall_structs.h:44:13: error: GNU-style inline assembly is disabled
#     __asm__ __volatile__("mov %%gs, %0" : "=r"(gs));
#             ^
# 1 error generated.
Patch6:		chromium-47.0.2526.80-pnacl-fgnu-inline-asm.patch
# Ignore broken nacl open fd counter
Patch7:		chromium-47.0.2526.80-nacl-ignore-broken-fd-counter.patch
# Use libusb_interrupt_event_handler from current libusbx (1.0.21-0.1.git448584a)
Patch9:		chromium-48.0.2564.116-libusb_interrupt_event_handler.patch
# Ignore deprecations in cups 2.2
# https://bugs.chromium.org/p/chromium/issues/detail?id=622493
Patch12:	chromium-55.0.2883.75-cups22.patch
# Add ICU Text Codec aliases (from openSUSE via Russian Fedora)
Patch14:	chromium-55.0.2883.75-more-codec-aliases.patch
# Use PIE in the Linux sandbox (from openSUSE via Russian Fedora)
Patch15:	chromium-55.0.2883.75-sandbox-pie.patch
# Enable ARM CPU detection for webrtc (from archlinux via Russian Fedora)
Patch16:	chromium-52.0.2743.82-arm-webrtc.patch
# Use /etc/chromium for master_prefs
Patch18:	chromium-52.0.2743.82-master-prefs-path.patch
# Disable MADV_FREE (if set by glibc)
# https://bugzilla.redhat.com/show_bug.cgi?id=1361157
Patch19:	chromium-52.0.2743.116-unset-madv_free.patch
# Use gn system files
Patch20:	chromium-54.0.2840.59-gn-system.patch
# Fix last commit position issue
# https://groups.google.com/a/chromium.org/forum/#!topic/gn-dev/7nlJv486bD4
Patch21:	chromium-53.0.2785.92-last-commit-position.patch
# Fix issue where timespec is not defined when sys/stat.h is included.
Patch22:	chromium-53.0.2785.92-boringssl-time-fix.patch
# I wouldn't have to do this if there was a standard way to append extra compiler flags
Patch24:	chromium-54.0.2840.59-nullfix.patch
# Add explicit includedir for jpeglib.h
Patch25:	chromium-54.0.2840.59-jpeg-include-dir.patch
# On i686, pass --no-keep-memory --reduce-memory-overheads to ld.
Patch26:	chromium-54.0.2840.59-i686-ld-memory-tricks.patch
# obj/content/renderer/renderer/child_frame_compositing_helper.o: In function `content::ChildFrameCompositingHelper::OnSetSurface(cc::SurfaceId const&, gfx::Size const&, float, cc::SurfaceSequence const&)':
# /builddir/build/BUILD/chromium-54.0.2840.90/out/Release/../../content/renderer/child_frame_compositing_helper.cc:214: undefined reference to `cc_blink::WebLayerImpl::setOpaque(bool)'
Patch27:	chromium-54.0.2840.90-setopaque.patch
# Use -fpermissive to build WebKit
Patch31:        chromium-56.0.2924.87-fpermissive.patch
# Fix issue with compilation on gcc7
# Thanks to Ben Noordhuis
Patch33:        chromium-56.0.2924.87-gcc7.patch
# Fix gn build
# https://chromium.googlesource.com/chromium/src.git/+/379e35f6f3eaa41a97f2659249509ca599749b27%5E%21/tools/gn/bootstrap/bootstrap.py
Patch35:        chromium-58.0.3029.81-fix-gn.patch
# Revert https://chromium.googlesource.com/chromium/src/+/b794998819088f76b4cf44c8db6940240c563cf4%5E%21/#F0
# https://bugs.chromium.org/p/chromium/issues/detail?id=712737
# https://bugzilla.redhat.com/show_bug.cgi?id=1446851
Patch36:        chromium-58.0.3029.96-revert-b794998819088f76b4cf44c8db6940240c563cf4.patch
# Correctly compile the stdatomic.h in ffmpeg with gcc 4.8
Patch37:        chromium-58.0.3029.81-ffmpeg-stdatomic.patch

### Chromium Tests Patches ###
Patch100:	chromium-46.0.2490.86-use_system_opus.patch
Patch101:	chromium-58.0.3029.81-use_system_harfbuzz.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%if 0%{tests}
Source1:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}-testdata.tar.xz
%endif
# https://chromium.googlesource.com/chromium/tools/depot_tools.git/+archive/7e7a454f9afdddacf63e10be48f0eab603be654e.tar.gz
Source2:	depot_tools.git-master.tar.gz

# We can assume gcc and binutils.
BuildRequires:	gcc-c++

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	gtk2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
BuildRequires:	libatomic
BuildRequires:	libcap-devel
BuildRequires:	libdrm-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libusb-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXScrnSaver-devel
BuildRequires:	libXtst-devel
BuildRequires:	nss-devel
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel
%if 0%{?tests}
BuildRequires:	pam-devel
# Tests needs X
BuildRequires:	Xvfb
BuildRequires:	liberation-sans-fonts
# For sandbox initialization
BuildRequires:	sudo
%endif

# Fedora turns on NaCl
# NaCl needs these
BuildRequires:	libstdc++-devel, openssl-devel
%if 0%{?nacl}
BuildRequires:	nacl-gcc, nacl-binutils, nacl-newlib
BuildRequires:	nacl-arm-gcc, nacl-arm-binutils, nacl-arm-newlib
# pNaCl needs this monster
# It's possible that someday this dep will stabilize, but
# right now, it needs to be updated everytime chromium bumps
# a major version.
BuildRequires:	chromium-native_client >= 52.0.2743.82
BuildRequires:	clang
%ifarch x86_64
# Really, this is what we want:
# BuildRequires:  glibc-devel(x86-32) libgcc(x86-32)
# But, koji only offers glibc32. Maybe that's enough.
# This BR will pull in either glibc.i686 or glibc32.
BuildRequires:	/lib/libc.so.6 /usr/lib/libc.so
%endif
%endif
# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
%if 0%{?bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
%else
# Not newer than 54 (at least not right now)
BuildRequires:	libicu-devel = 54.1
%endif
BuildRequires:	libjpeg-devel
# BuildRequires:	libpng-devel
%if 0
# see https://code.google.com/p/chromium/issues/detail?id=501318
BuildRequires:	libsrtp-devel >= 1.4.4
%endif
BuildRequires:	libudev-devel
%if %{bundlelibusbx}
# Do nothing
%else
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
%endif
# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
# Same is true for libwebp.
BuildRequires:	libxslt-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
%if %{bundleopus}
# Do nothing
%else
BuildRequires:	opus-devel
%endif
BuildRequires:	perl(Switch)
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	python-beautifulsoup4
BuildRequires:	python-BeautifulSoup
BuildRequires:	python-html5lib
BuildRequires:	python-jinja2
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
BuildRequires:	python-simplejson
%if 0%{?bundlere2}
# Using bundled bits, do nothing.
%else
BuildRequires:	re2-devel >= 20160401
%endif
BuildRequires:	speech-dispatcher-devel
BuildRequires:	yasm
BuildRequires:	pkgconfig(gnome-keyring-1)
# remote desktop needs this
BuildRequires:	pam-devel
BuildRequires:	systemd

ExclusiveArch:	x86_64 i686

Provides:   %{cname}-libs-media = %{version}-%{release}
Provides:   %{cname}-libs-media%{_isa}  = %{version}-%{release}
Obsoletes:  %{cname}-libs-media

%description
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.


%prep
%setup -q -T -c -n depot_tools -a 2
%if 0%{tests}
%setup -q -n chromium-%{version} -b 1
%else
%setup -q -n chromium-%{version}
%endif

### Chromium Fedora Patches ###
%patch0 -p1 -b .gcc5
%patch1 -p1 -b .pathmax
%patch2 -p1 -b .addrfix
%patch4 -p1 -b .notest
# %%patch6 -p1 -b .gnu-inline
%patch7 -p1 -b .ignore-fd-count
%patch9 -p1 -b .modern-libusbx
%patch12 -p1 -b .cups22
%patch14 -p1 -b .morealiases
%patch15 -p1 -b .sandboxpie
%patch16 -p1 -b .armwebrtc
%patch18 -p1 -b .etc
# %%patch19 -p1 -b .madv_free
%patch20 -p1 -b .gnsystem
%patch21 -p1 -b .lastcommit
%patch22 -p1 -b .timefix
%patch24 -p1 -b .nullfix
%patch25 -p1 -b .jpegfix
%patch26 -p1 -b .ldmemory
%patch27 -p1 -b .setopaque
%patch31 -p1 -b .permissive
%patch33 -p1 -b .gcc7
%patch35 -p1 -b .fixgn
%patch36 -p1 -b .revert
%patch37 -p1 -b .ffmpeg-stdatomic

### Chromium Tests Patches ###
%patch100 -p1 -b .use_system_opus
%patch101 -p1 -b .use_system_harfbuzz

%if 0%{?asan}
export CC="clang"
export CXX="clang++"
%else
export CC="gcc"
export CXX="g++"
%endif
export AR="ar"
export RANLIB="ranlib"

%if 0%{?nacl}
# prep the nacl tree
mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib
cp -a --no-preserve=context /usr/%{_arch}-nacl/* out/Release/gen/sdk/linux_x86/nacl_x86_newlib

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib
cp -a --no-preserve=context /usr/arm-nacl/* out/Release/gen/sdk/linux_x86/nacl_arm_newlib

# Not sure if we need this or not, but better safe than sorry.
pushd out/Release/gen/sdk/linux_x86
ln -s nacl_x86_newlib nacl_x86_newlib_raw
ln -s nacl_arm_newlib nacl_arm_newlib_raw
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_x86_newlib/bin
ln -s /usr/bin/x86_64-nacl-gcc gcc
ln -s /usr/bin/x86_64-nacl-gcc x86_64-nacl-gcc
ln -s /usr/bin/x86_64-nacl-g++ g++
ln -s /usr/bin/x86_64-nacl-g++ x86_64-nacl-g++
# ln -s /usr/bin/x86_64-nacl-ar ar
ln -s /usr/bin/x86_64-nacl-ar x86_64-nacl-ar
# ln -s /usr/bin/x86_64-nacl-as as
ln -s /usr/bin/x86_64-nacl-as x86_64-nacl-as
# ln -s /usr/bin/x86_64-nacl-ranlib ranlib
ln -s /usr/bin/x86_64-nacl-ranlib x86_64-nacl-ranlib
# Cleanups
rm addr2line
ln -s /usr/bin/x86_64-nacl-addr2line addr2line
rm c++filt
ln -s /usr/bin/x86_64-nacl-c++filt c++filt
rm gprof
ln -s /usr/bin/x86_64-nacl-gprof gprof
rm readelf
ln -s /usr/bin/x86_64-nacl-readelf readelf
rm size
ln -s /usr/bin/x86_64-nacl-size size
rm strings
ln -s /usr/bin/x86_64-nacl-strings strings
popd

mkdir -p out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
pushd out/Release/gen/sdk/linux_x86/nacl_arm_newlib/bin
ln -s /usr/bin/arm-nacl-gcc gcc
ln -s /usr/bin/arm-nacl-gcc arm-nacl-gcc
ln -s /usr/bin/arm-nacl-g++ g++
ln -s /usr/bin/arm-nacl-g++ arm-nacl-g++
ln -s /usr/bin/arm-nacl-ar arm-nacl-ar
ln -s /usr/bin/arm-nacl-as arm-nacl-as
ln -s /usr/bin/arm-nacl-ranlib arm-nacl-ranlib
popd

touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_x86_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_x86_newlib/nacl_x86_newlib.json
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.untar out/Release/gen/sdk/linux_x86/nacl_arm_newlib/stamp.prep
touch out/Release/gen/sdk/linux_x86/nacl_arm_newlib/nacl_arm_newlib.json

pushd out/Release/gen/sdk/linux_x86/
mkdir -p pnacl_newlib pnacl_translator
# Might be able to do symlinks here, but eh.
cp -a --no-preserve=context /usr/pnacl_newlib/* pnacl_newlib/
cp -a --no-preserve=context /usr/pnacl_translator/* pnacl_translator/
for i in lib/libc.a lib/libc++.a lib/libg.a lib/libm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/x86_64_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/i686_bc-nacl/$i
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/le32-nacl/$i
done

for i in lib/libpthread.a lib/libnacl.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/le32-nacl/$i
done

for i in lib/clang/3.7.0/lib/x86_64_bc-nacl/libpnaclmm.a lib/clang/3.7.0/lib/i686_bc-nacl/libpnaclmm.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

for i in lib/clang/3.7.0/lib/le32-nacl/libpnaclmm.a lib/clang/3.7.0/lib/le32-nacl/libgcc.a; do
	/usr/pnacl_newlib/bin/pnacl-ranlib pnacl_newlib/$i
done

popd

mkdir -p native_client/toolchain/.tars/linux_x86
touch native_client/toolchain/.tars/linux_x86/pnacl_translator.json

pushd native_client/toolchain
ln -s ../../out/Release/gen/sdk/linux_x86 linux_x86
popd

mkdir -p third_party/llvm-build/Release+Asserts/bin
pushd third_party/llvm-build/Release+Asserts/bin
ln -s /usr/bin/clang clang
popd
%endif

CHROMIUM_BROWSER_GN_DEFINES=""
CHROMIUM_BROWSER_GN_DEFINES+=' is_debug=false'
%ifarch x86_64
CHROMIUM_BROWSER_GN_DEFINES+=' system_libdir="lib64"'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' google_api_key="%{api_key}" google_default_client_id="%{default_client_id}" google_default_client_secret="%{default_client_secret}"'
CHROMIUM_BROWSER_GN_DEFINES+=' is_clang=false use_sysroot=false use_gio=true use_pulseaudio=true icu_use_data_file=true'
%if 0%{?nonacl}
CHROMIUM_BROWSER_GN_DEFINES+=' enable_nacl=false'
%endif
CHROMIUM_BROWSER_GN_DEFINES+=' ffmpeg_branding="ChromeOS" proprietary_codecs=true'
CHROMIUM_BROWSER_GN_DEFINES+=' is_component_ffmpeg=true is_component_build=true'
CHROMIUM_BROWSER_GN_DEFINES+=' remove_webcore_debug_symbols=true enable_hangout_services_extension=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_hotwording=false use_aura=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_webrtc=true enable_widevine=true'
CHROMIUM_BROWSER_GN_DEFINES+=' use_gold=false'
CHROMIUM_BROWSER_GN_DEFINES+=' use_gtk3=false'
# CHROMIUM_BROWSER_GN_DEFINES+=' use_system_libjpeg=true'
CHROMIUM_BROWSER_GN_DEFINES+=' treat_warnings_as_errors=false'
export CHROMIUM_BROWSER_GN_DEFINES

export CHROMIUM_BROWSER_GYP_DEFINES="\
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="%{api_key}" \
	-Dgoogle_default_client_id="%{default_client_id}" \
	-Dgoogle_default_client_secret="%{default_client_secret}" \
%if 0%{?asan}
	-Dasan=1 \
	-Dclang=1 \
	-Dhost_clang=1 \
	-Dclang_dynlib_flags="" \
	-Dclang_plugin_args="" \
	-Dclang_chrome_plugins_flags="" \
%else
	-Dclang=0 \
        -Dhost_clang=0 \
%endif
	-Ddisable_glibc=1 \
	-Dlinux_fpic=1 \
	-Ddisable_sse2=1 \
%if 0%{?nonacl}
	-Ddisable_nacl=1 \
%else
	-Ddisable_newlib_untar=1 \
	-Ddisable_pnacl_untar=1 \
	-Dpnacl_newlib_toolchain=out/Release/gen/sdk/linux_x86/pnacl_newlib/ \
	-Dpnacl_translator_dir=/usr/pnacl_translator \
%endif
	\
	-Duse_gconf=0 \
	-Duse_gio=1 \
	-Duse_gnome_keyring=1 \
	-Duse_pulseaudio=1 \
	-Duse_system_bzip2=1 \
	-Duse_system_flac=1 \
%if 0%{?bundleharfbuzz}
	-Duse_system_harfbuzz=0 \
%else
	-Duse_system_harfbuzz=1 \
%endif
%if 0%{?bundleicu}
	-Duse_system_icu=0 \
%else
	-Duse_system_icu=1 \
%endif
	-Dicu_use_data_file_flag=1 \
	-Duse_system_libevent=0 \
	-Duse_system_libjpeg=1 \
	-Duse_system_libpng=1 \
%if %{bundlelibusbx}
	-Duse_system_libusb=0 \
%else
	-Duse_system_libusb=1 \
%endif
	-Duse_system_libxml=1 \
	-Duse_system_libxslt=1 \
%if %{bundleopus}
	-Duse_system_opus=0 \
%else
	-Duse_system_opus=1 \
%endif
	-Duse_system_protobuf=0 \
%if 0%{?bundlere2}
%else
	-Duse_system_re2=1 \
%endif
	-Duse_system_libsrtp=0 \
	-Duse_system_xdg_utils=1 \
	-Duse_system_yasm=1 \
	-Duse_system_zlib=0 \
	\
	-Dlinux_link_libspeechd=1 \
	-Dlinux_link_gnome_keyring=1 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chromium-browser \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_bundled_binutils=0 \
	-Dlinux_use_bundled_gold=0 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	\
	-Dusb_ids_path=/usr/share/hwdata/usb.ids \
%if 0%{?fedora}
	-Dlibspeechd_h_prefix=speech-dispatcher/ \
%endif
	\
    -Dffmpeg_branding=ChromeOS \
    -Dproprietary_codecs=1 \
	-Dbuild_ffmpegsumo=1 \
	-Dffmpeg_component=shared_library \
	\
	-Dno_strict_aliasing=1 \
	-Dv8_no_strict_aliasing=1 \
	\
	-Dremove_webcore_debug_symbols=1 \
	-Dlogging_like_official_build=1 \
	-Denable_hotwording=0 \
	-Duse_aura=1 \
	-Denable_hidpi=1 \
	-Denable_touch_ui=1 \
	-Denable_pepper_cdms=1 \
	-Denable_webrtc=1 \
	-Denable_widevine=1 \
	-Dtoolkit_uses_gtk=0 \
	\
	-Dcomponent=shared_library \
	-Duse_sysroot=0 \
	-Drelease_extra_cflags="-fno-delete-null-pointer-checks" \
	-Dwerror= -Dsysroot="

export PATH=$PATH:%{_builddir}/depot_tools

%if %{use_gn}
build/linux/unbundle/replace_gn_files.py --system-libraries \
	flac \
%if 0%{?bundleharfbuzz}
%else
	harfbuzz-ng \
%endif
%if 0%{?bundleicu}
%else
	icu \
%endif
%if 0
	libevent \
%endif
%if %{bundlelibusbx}
%else
	libusb \
%endif
	libxml \
	libxslt \
%if %{bundleopus}
%else
	opus \
%endif
%if 0%{?bundlere2}
%else
	re2 \
%endif
	yasm

tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "$CHROMIUM_BROWSER_GN_DEFINES"
%{target}/gn gen --args="$CHROMIUM_BROWSER_GN_DEFINES" %{target}
%else
# Update gyp files according to our configuration
# If you will change something in the configuration please update it
# for build/gyp_chromium as well (and vice versa).
build/linux/unbundle/replace_gyp_files.py $CHROMIUM_BROWSER_GYP_DEFINES

build/gyp_chromium \
	--depth . \
%if 0%{?asan}
	-Drelease_extra_cflags="-O1 -fno-inline-functions -fno-inline" \
%endif
	$CHROMIUM_BROWSER_GYP_DEFINES
%endif

# fix arm gcc
sed -i 's|arm-linux-gnueabihf-|arm-linux-gnu-|g' build/toolchain/linux/BUILD.gn

%build

%if %{?tests}
export CHROMIUM_BROWSER_UNIT_TESTS="\
	media_unittests \
	"
%else
export CHROMIUM_BROWSER_UNIT_TESTS=
%endif


%global target out/Release

../depot_tools/ninja -C %{target} -vvv media $CHROMIUM_BROWSER_UNIT_TESTS


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{chromium_path}

pushd %{target}
cp -a libffmpeg.so* %{buildroot}%{chromium_path}
cp -a libmedia.so* %{buildroot}%{chromium_path}
popd

%check
%if 0%{tests}
%if 0%{?tests_force_display}
	export DISPLAY=:0
%else
	Xvfb :9 -screen 0 1024x768x24 &

	export XVFB_PID=$!
	export DISPLAY=:9
%endif
	export LC_ALL="en_US.utf8"

	sleep 5

	# Run tests and disable the failed ones
	pushd %{target}
	(

	./media_unittests \
	)
	popd

	if [ -n "$XVFB_PID" ]; then
		kill $XVFB_PID
		unset XVFB_PID
		unset DISPLAY
	fi
%endif

%files
%doc AUTHORS
%license LICENSE
%{chromium_path}/libffmpeg.so*
%{chromium_path}/libmedia.so*

%changelog
* Fri Mar  3 2017 No One <noone AT nowhere DOT com> 58.0.3029.110-2
- update to 58.0.3029.110

* Fri Mar  3 2017 No One <noone AT nowhere DOT com> 56.0.2924.87-1
- update to 56.0.2924.87

* Fri Dec 2 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> 54.0.2840.100-1
- Trimming out all unnecessary builds and tests
- Update to 54.0.2840.100

* Mon Nov 28 2016 Jeremy Newton <alexjnewt AT hotmail DOT com> 54.0.2840.90-1
- Initial package
