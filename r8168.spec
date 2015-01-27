# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

%if "%{_alt_kernel}" != "%{nil}"
%if 0%{?build_kernels:1}
%{error:alt_kernel and build_kernels are mutually exclusive}
exit 1
%endif
%global		_build_kernels		%{alt_kernel}
%else
%global		_build_kernels		%{?build_kernels:,%{?build_kernels}}
%endif

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		kbrs	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo "BuildRequires:kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2" ; done)
%define		kpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%kernel_pkg ; done)
%define		bkpkg	%(echo %{_build_kernels} | tr , '\\n' | while read n ; do echo %%undefine alt_kernel ; [ -z "$n" ] || echo %%define alt_kernel $n ; echo %%build_kernel_pkg ; done)

%define		rel	2
%define		pname	r8168
Summary:	Linux driver for RTL8111/8168B PCI Express Gigabit Ethernet controllers
Summary(pl.UTF-8):	Linuksowy sterownik dla kart sieciowych RTL8111/8168B PCI Express Gigabit Ethernet
Name:		%{pname}%{_alt_kernel}
Version:	8.038.00
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
URL:		http://www.realtek.com.tw/
# Check for new versions at
# http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=13&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false
# unfortunately this download is not DF-friendly.
Source0:	%{pname}-%{version}.tar.bz2
# Source0-md5:	fe2962824587070a2ec53f77e40b0fea
Patch0:		linux-3.15.patch
Patch1:		linux-3.16.patch
BuildRequires:	rpmbuild(macros) >= 1.678
%{expand:%kbrs}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%description
Driver (Linux kernel module) for RTL8111/8168B PCI Express Gigabit
Ethernet controllers.

%description -l pl.UTF-8
Sterownik (moduł jądra Linuksa) dla kart sieciowych RTL8111/8168B PCI
Express Gigabit Ethernet.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-r8168\
Summary:	Linux kernel module for RTL8111/8168B PCI Express Gigabit Ethernet controllers\
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart sieciowych RTL8111/8168B PCI Express Gigabit Ethernet\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-net-r8168\
Driver (Linux kernel module) for RTL8111/8168B PCI Express Gigabit\
Ethernet controllers.\
\
%description -n kernel%{_alt_kernel}-net-r8168 -l pl.UTF-8\
Sterownik (moduł jądra Linuksa) dla kart sieciowych RTL8111/8168B PCI\
Express Gigabit Ethernet.\
\
%files -n kernel%{_alt_kernel}-net-r8168\
%defattr(644,root,root,755)\
%doc README\
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-r8168\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-r8168\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m r8168 -C src KERNELRELEASE=%{_kernel_ver}\
%install_kernel_modules -D installed -m src/r8168 -d kernel/drivers/net\
%{nil}

%{expand:%kpkg}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{expand:%bkpkg}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
