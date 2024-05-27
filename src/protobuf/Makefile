SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS += -e

MAIN_TARGET = libprotobuf32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb
DERIVED_TARGETS = protobuf-compiler_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotobuf-dev_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotobuf-lite32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotoc32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotoc-dev_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					python3-protobuf_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					ruby-google-protobuf_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	# Remove any stale files
	rm -rf protobuf-$(PROTOBUF_VERSION)

	dget -u protobuf_$(PROTOBUF_VERSION_FULL).dsc http://deb.debian.org/debian/pool/main/p/protobuf/protobuf_$(PROTOBUF_VERSION_FULL).dsc

	pushd protobuf-$(PROTOBUF_VERSION)

ifeq ($(CROSS_BUILD_ENVIRON), y)
	sed -i '/cp -Rv src\/.libs debian\/native_protoc/{n;n;n;n;n;s/.*/&\n\tcp -Rv src\/.libs debian\/native_protoc/}' debian/rules
	sed -i '0,/cp -Rv src\/.libs debian\/native_protoc/{//d;}' debian/rules
	extconf_file=$(find . -type f -name extconf.rb -path '*/ruby/ext/google/protobuf_c/extconf.rb' 2>/dev/null)
	if [ -f "$extconf_file" ]; then
	if ! grep -qF "Add arm-linux-gnueabihf build configuration" $extconf_file; then
	echo "Adding ARM build configuration to $extconf_file"
	echo "# Add arm-linux-gnueabihf build configuration" >> $extconf_file;
	echo "makefile_content = File.read('Makefile')" >> $extconf_file;
	echo "makefile_content.gsub!(/^arch\s*=\s*x86_64-linux-gnu$/, \"arch = arm-linux-gnueabihf\")" >> $extconf_file;
	echo "makefile_content.gsub!(/^arch_hdrdir\s*=\s*\/usr\/include\/x86_64-linux-gnu\/ruby-2\.7\.0$/, \"arch_hdrdir = /usr/include/arm-linux-gnueabihf/ruby-2.7.0\")" >> $extconf_file;
	echo "File.open('Makefile', 'w') { |file| file.puts makefile_content }" >> $extconf_file;
	fi
	fi
	
	dpkg-buildpackage -us -uc -b -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
	
	if [ -f "$extconf_file" ]; then
	if ! grep -qF "Add arm-linux-gnueabihf build configuration" $extconf_file; then
	sed -i '/Add arm-linux-gnueabihf build configuration/,$d' $extconf_file
	fi
	fi
	dpkg-buildpackage -us -uc -b -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
else
	dpkg-buildpackage -us -uc -b -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
endif

	popd

	mv $(DERIVED_TARGETS) $* $(DEST)/

$(addprefix $(DEST)/, $(DERIVED_TARGETS)): $(DEST)/% : $(DEST)/$(MAIN_TARGET)
