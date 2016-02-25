#ifdef FROM_CMSSW
#include "../interface/TreeWrapper.h"
#include "../interface/TreeWrapperAccessor.h"
#else
#include <TreeWrapper.h>
#include <TreeWrapperAccessor.h>
#endif

namespace ROOT {
    TreeWrapperAccessor::TreeWrapperAccessor(ROOT::TreeWrapper* wrap) {
        wrapper = wrap;
    }

    TTree* TreeWrapperAccessor::tree() {
        return wrapper->m_tree;
    }

    uint64_t TreeWrapperAccessor::entry() {
        return wrapper->m_entry;
    }
}
