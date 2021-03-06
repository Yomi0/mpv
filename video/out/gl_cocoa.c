/*
 * MPlayer is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * MPlayer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with MPlayer; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * You can alternatively redistribute this file and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 */

#include "cocoa_common.h"
#include "gl_common.h"

static void gl_clear(void *ctx)
{
    struct GL *gl = ctx;
    gl->ClearColor(0.0f, 0.0f, 0.0f, 0.0f);
    gl->Clear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

static bool config_window_cocoa(struct MPGLContext *ctx, int flags)
{
    int rv = vo_cocoa_config_window(ctx->vo, flags,
                                    ctx->requested_gl_version >= MPGL_VER(3, 0));
    if (rv != 0)
        return false;

    mpgl_load_functions(ctx->gl, (void *)vo_cocoa_glgetaddr, NULL, ctx->vo->log);

    ctx->depth_r = vo_cocoa_cgl_color_size(ctx->vo);
    ctx->depth_g = vo_cocoa_cgl_color_size(ctx->vo);
    ctx->depth_b = vo_cocoa_cgl_color_size(ctx->vo);

    if (!ctx->gl->SwapInterval)
        ctx->gl->SwapInterval = vo_cocoa_swap_interval;

    vo_cocoa_register_gl_clear_callback(ctx->vo, ctx->gl, gl_clear);

    return true;
}

static void releaseGlContext_cocoa(MPGLContext *ctx)
{
}

static void swapGlBuffers_cocoa(MPGLContext *ctx)
{
    vo_cocoa_swap_buffers(ctx->vo);
}

static void set_current_cocoa(MPGLContext *ctx, bool current)
{
    vo_cocoa_set_current_context(ctx->vo, current);
}

void mpgl_set_backend_cocoa(MPGLContext *ctx)
{
    ctx->config_window = config_window_cocoa;
    ctx->releaseGlContext = releaseGlContext_cocoa;
    ctx->swapGlBuffers = swapGlBuffers_cocoa;
    ctx->vo_init = vo_cocoa_init;
    ctx->register_resize_callback = vo_cocoa_register_resize_callback;
    ctx->vo_uninit = vo_cocoa_uninit;
    ctx->vo_control = vo_cocoa_control;
    ctx->set_current = set_current_cocoa;
}
