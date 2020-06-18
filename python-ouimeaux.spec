%global srcname ouimeaux

# This is the correct folder for firewalld service files, even on x86_64
# It is not used for shared objects
%global fw_services %{_prefix}/lib/firewalld/services

Name: python-%{srcname}
Version: 0.8.2
Release: 7%{?dist}
Summary: Open source control for Belkin WeMo devices

License: BSD and ASL 2.0
Url: https://github.com/iancmcc/ouimeaux
Source0: https://github.com/iancmcc/%{srcname}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: README.firewall
Source2: ouimeaux.xml

# https://patch-diff.githubusercontent.com/raw/iancmcc/ouimeaux/pull/204.patch
Patch0:  python-ouimeaux-cElementTree.patch
# https://github.com/knight-of-ni/ouimeaux/commit/2cea05f127499f42179b3699866b8e1444761b9f.patch
Patch1:  python-ouimeaux-unbundle-pysignals.patch

# https://github.com/iancmcc/ouimeaux/commit/607bfb3627c32937ca7e542e462053bbb124ee06.patch
Patch2:  python-ouimeaux-move-statechange.patch

BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: findutils
BuildRequires: sed
BuildRequires: coreutils
BuildRequires: firewalld-filesystem

# Required for check
BuildRequires: %{py3_dist gevent} >= 1.3
BuildRequires: %{py3_dist requests} >= 2.3.0
BuildRequires: %{py3_dist pyyaml}
BuildRequires: %{py3_dist six}
BuildRequires: %{py3_dist future}
BuildRequires: %{py3_dist pysignals}

%global _description %{expand:
Open source control for Belkin WeMo devices

- Supports WeMo Switch, Light Switch, Insight Switch and Motion
- Command-line tool to discover and control devices in your environment
- REST API to obtain information and perform actions on devices
- Simple responsive Web app provides device control on mobile
- Python API to interact with device at a low level
}

%description %_description

%package -n python3-%{srcname}
Requires: firewalld-filesystem
Requires: webfts
Requires: js-jquery1
Requires: %{py3_dist pysignals}
Requires(post): firewalld-filesystem

Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description

%prep
%autosetup -p 1 -n %{srcname}-%{version}

install -pm 0644 %{SOURCE1} .

# Dont build examples, add to docs instead
mv ouimeaux/examples examples
rm examples/__init__.py

# Remove python shebang from __init__.py
sed -i -e '/^#!\//, 1d' ouimeaux/__init__.py

# fix python shebang and non-executable-script errors
find \( -name device.py -or -name service.py -or -name watch.py \) -type f -exec chmod +x {} \; -exec sed -i 's\^#!/usr/bin/env python$\#!%{python3}\' {} \;

%build
%py3_build

%install
%py3_install

# replace glyphicons-halflings with links to the packaged file with the same name
for ftype in woff ttf svg eot; do
  ln -sf /var/www/webfts/fonts/glyphicons-halflings-regular.$ftype %{buildroot}%{python3_sitelib}/%{srcname}/server/static/fonts/glyphicons-halflings-regular.$ftype
done

# replace jquery with links to the packaged files with the same name
ln -sf /usr/share/javascript/jquery/1.12.4/jquery.js %{buildroot}%{python3_sitelib}/%{srcname}/server/static/lib/jquery/jquery.js
ln -sf /usr/share/javascript/jquery/1.12.4/jquery.min.js %{buildroot}%{python3_sitelib}/%{srcname}/server/static/lib/jquery/jquery.min.js

# Install firewalld config
mkdir -p %{buildroot}%{fw_services}
install -pm 0644 %{SOURCE2} %{buildroot}%{fw_services}/

%post
%{?firewalld_reload}

%check
%{python3} setup.py test

%files -n python3-%{srcname}
%license LICENSE
%doc README.md HISTORY.rst AUTHORS.rst CONTRIBUTING.rst README.firewall examples/
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/
%{_bindir}/wemo
%{fw_services}/%{srcname}.xml

%changelog
* Wed Jun 17 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-7
- unbundle statechange class from pysignals

* Wed Jun 17 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-6
- unbundle pysignals into separate pacakge

* Tue Jun 16 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-5
- patch for python 3.9 compatbility
- move runtime requirements into subpackage
- unbundle glyphicons-halflings
- bootstrap java files are ASL 2.0 license
- unbundle jquery

* Mon Jun 15 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-4
- Author updated releases page to match version in source, dropping git commit

* Mon May 25 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-3.git.6b6984b
- Define fw_services macro

* Mon May 25 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-2.git.6b6984b
- Add firewalld config and readme
- move examples to docs

* Sun May 17 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 0.8.2-1.git.6b6984b
- Initial package

