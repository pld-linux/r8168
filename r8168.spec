#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif

%define		rel	1
Summary:	Linux driver for RTL8111/8168B PCI Express Gigabit Ethernet controllers
Summary(pl.UTF-8):	Linuksowy sterownik dla kart sieciowych RTL8111/8168B PCI Express Gigabit Ethernet
Name:		r8168
Version:	8.003.00
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
URL:		http://www.realtek.com.tw/
Source0:	ftp://202.65.194.212/cn/nic/r8168-%{version}.tar.bz2
# Source0-md5:	f22797f85eaba7d657365945aa92fecf
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Driver (Linux kernel module) for RTL8111/8168B PCI Express Gigabit
Ethernet controllers.

%description -l pl.UTF-8
Sterownik (moduł jądra Linuksa) dla kart sieciowych RTL8111/8168B PCI
Express Gigabit Ethernet.

%package -n kernel%{_alt_kernel}-net-r8168
Summary:	Linux kernel module for RTL8111/8168B PCI Express Gigabit Ethernet controllers
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart sieciowych RTL8111/8168B PCI Express Gigabit Ethernet
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-net-r8168
Driver (Linux kernel module) for RTL8111/8168B PCI Express Gigabit
Ethernet controllers.

%description -n kernel%{_alt_kernel}-net-r8168 -l pl.UTF-8
Sterownik (moduł jądra Linuksa) dla kart sieciowych RTL8111/8168B PCI
Express Gigabit Ethernet.

%prep
%setup -q -n r8168-%{version}

%build
%if %{with kernel}
%build_kernel_modules -m r8168 -C src
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with kernel}
%install_kernel_modules -m src/r8168 -d kernel/drivers/net
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-r8168
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-r8168
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-net-r8168
%defattr(644,root,root,755)
%doc release_note.txt readme
/lib/modules/%{_kernel_ver}/kernel/drivers/net/*.ko*
%endif
