# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	2
%define		pname	r8168
Summary:	Linux driver for RTL8111/8168B PCI Express Gigabit Ethernet controllers
Summary(pl.UTF-8):	Linuksowy sterownik dla kart sieciowych RTL8111/8168B PCI Express Gigabit Ethernet
Name:		%{pname}%{_alt_kernel}
Version:	8.042.00
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL
Group:		Base/Kernel
URL:		http://www.realtek.com.tw/
# Check for new versions at
# http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=13&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false
# unfortunately this download is not DF-friendly.
Source0:	%{pname}-%{version}.tar.bz2
# Source0-md5:	2c583809d1ebf26ed7f5e775c83e68e0
Patch0:		linux-4.5.patch
Patch1:		linux-4.7.patch
Patch2:		linux-4.11.patch
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build >= 3:2.6.20.2}
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

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{expand:%build_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
