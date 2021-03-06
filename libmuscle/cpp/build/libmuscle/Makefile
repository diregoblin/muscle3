# Get source paths
hdrdir := $(CURDIR)/../../src
srcdir := $(CURDIR)/../../src/libmuscle
srcdirs := $(srcdir) $(srcdir)/mcp $(srcdir)/bindings
objdir := $(CURDIR)/objs

VPATH := $(srcdir)
source_files := $(foreach dir,$(srcdirs),$(wildcard $(dir)/*.cpp))
objects := $(source_files:$(srcdir)%.cpp=$(objdir)%.o)
lobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.lo)
dobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.do)
dlobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.dlo)
mobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.mo)
mlobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.mlo)
mdobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.mdo)
mdlobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.mdlo)

deps := $(source_files:$(srcdir)%.cpp=$(objdir)%.d)

prod_libs := libmuscle.a libmuscle.so
debug_libs := libmuscle_d.a libmuscle_d.so

ifdef MUSCLE_ENABLE_MPI
prod_libs += libmuscle_mpi.a libmuscle_mpi.so
debug_libs += libmuscle_mpi_d.a libmuscle_mpi_d.so
endif

all_libs := $(prod_libs)

ifdef MUSCLE_ENABLE_DEBUG
all_libs += $(debug_libs)
endif

header_root := $(CURDIR)/../../src
CXXFLAGS += -I$(header_root)

public_headers := libmuscle/data.hpp libmuscle/data.tpp libmuscle/instance.hpp
public_headers += libmuscle/libmuscle.hpp libmuscle/message.hpp
public_headers += libmuscle/ports_description.hpp libmuscle/util.hpp libmuscle/util.tpp
installed_headers := $(public_headers:%=$(PREFIX)/include/%)

CXXFLAGS += -Wall -pedantic -std=c++14
export CXXFLAGS
MPICXX := mpic++
export MPICXX
MPIFLAGS := -DMUSCLE_ENABLE_MPI
export MPIFLAGS
DEBUGFLAGS := -g
export DEBUGFLAGS


.PHONY: all
all: $(all_libs) version.h

.PHONY: tests
tests: libmuscle_d.a version.h
	$(MAKE) -C tests tests

.PHONY: test
test: tests
	$(MAKE) -C tests test

.PHONY: clean
clean:
	rm -f libmuscle.a libmuscle.so libmuscle_d.a libmuscle_d.so version.h
	rm -f libmuscle_mpi.a libmuscle_mpi.so libmuscle_mpi_d.a libmuscle_mpi_d.so
	rm -rf $(objdir)
	$(MAKE) -C tests clean

.PHONY: distclean
distclean: clean
	$(MAKE) -C tests distclean

.PHONY: install
install: all $(installed_headers)
	@echo
	@echo Installing libmuscle to $(PREFIX)
	@mkdir -p $(PREFIX)/lib
	cp libmuscle*.a $(PREFIX)/lib
	cp libmuscle*.so $(PREFIX)/lib


cleantargets := clean distclean
ifeq "$(filter $(MAKECMDGOALS),$(cleantargets))" ""

# Dependencies
$(info pcextra: $(PKG_CONFIG_EXTRA_DIRS))
CXXFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --cflags protobuf)
CXXFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --cflags grpc grpc++)
CXXFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --cflags msgpack)

LDFLAGS += -L$(CURDIR)/../muscle_manager_protocol -lmmp -L$(CURDIR)/../ymmsl -lymmsl
LDFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --libs protobuf)
LDFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --libs grpc grpc++)
LDFLAGS += $(shell export PKG_CONFIG_PATH=$(PKG_CONFIG_EXTRA_DIRS) ; pkg-config --libs msgpack)

# Automatic header dependencies
-include $(deps)


# Make version.h
version_template := $(srcdir)/version.h.in
version_file := $(CURDIR)/../../../../VERSION
major_version := $(shell sed -e 's/^\([0-9]*\)\..*/\1/' $(version_file))
minor_version := $(shell sed -e 's/^[0-9]*\.\([0-9]*\)\..*/\1/' $(version_file))
patch_version := $(shell sed -e 's/^[0-9]*\.[0-9]*\.\([0-9]*\).*/\1/' $(version_file))

endif


$(objdir)/%.d: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -E -MM -MT $(@:.d=.o) $< -o $@

$(objdir)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

# depends on .o to daisy-chain automatic dependencies
$(objdir)/%.lo: %.cpp $(objdir)/%.o
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -fPIC -c $< -o $@

# depends on .o to daisy-chain automatic dependencies
$(objdir)/%.do: %.cpp $(objdir)/%.o
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(DEBUGFLAGS) $(CXXFLAGS) -c $< -o $@

# depends on .o to daisy-chain automatic dependencies
$(objdir)/%.dlo: %.cpp $(objdir)/%.o
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(DEBUGFLAGS) $(CXXFLAGS) -fPIC -c $< -o $@

$(objdir)/%.mo: %.cpp
	@mkdir -p $(@D)
	$(MPICXX) $(CPPFLAGS) $(CXXFLAGS) $(MPIFLAGS) -c $< -o $@

$(objdir)/%.mlo: %.cpp
	@mkdir -p $(@D)
	$(MPICXX) $(CPPFLAGS) $(CXXFLAGS) $(MPIFLAGS) -fPIC -c $< -o $@

$(objdir)/%.mdo: %.cpp
	@mkdir -p $(@D)
	$(MPICXX) $(CPPFLAGS) $(DEBUGFLAGS) $(CXXFLAGS) $(MPIFLAGS) -c $< -o $@

$(objdir)/%.mdlo: %.cpp
	@mkdir -p $(@D)
	$(MPICXX) $(CPPFLAGS) $(DEBUGFLAGS) $(CXXFLAGS) $(MPIFLAGS) -fPIC -c $< -o $@


version.h: $(version_template) $(version_file)
	cp $(version_template) $@
	sed -i -e 's/@PROJECT_VERSION_MAJOR@/$(major_version)/' $@
	sed -i -e 's/@PROJECT_VERSION_MINOR@/$(minor_version)/' $@
	sed -i -e 's/@PROJECT_VERSION_PATCH@/$(patch_version)/' $@

libmuscle.a: $(objects)
	ar rcs $@ $^

libmuscle.so: $(lobjects)
	$(CXX) -shared -Wl,--version-script=libmuscle.version -o $@ $^ $(LDFLAGS)

libmuscle_d.a: $(dobjects)
	ar rcs $@ $^

libmuscle_d.so: $(dlobjects)
	$(CXX) -shared -Wl,--version-script=libmuscle.version -o $@ $^ $(LDFLAGS)

libmuscle_mpi.a: $(mobjects)
	ar rcs $@ $^

libmuscle_mpi.so: $(mlobjects)
	$(CXX) -shared -Wl,--version-script=libmuscle.version -o $@ $^ $(LDFLAGS)

libmuscle_mpi_d.a: $(mdobjects)
	ar rcs $@ $^

libmuscle_mpi_d.so: $(mdlobjects)
	$(CXX) -shared -Wl,--version-script=libmuscle.version -o $@ $^ $(LDFLAGS)

$(PREFIX)/include/%.hpp: $(hdrdir)/%.hpp
	@mkdir -p $(@D)
	cp $< $@

$(PREFIX)/include/%.tpp: $(hdrdir)/%.tpp
	@mkdir -p $(@D)
	cp $< $@

